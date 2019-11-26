#
#  Copyright (c) 2018-2019, Texas Instruments Incorporated
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#  *  Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#  *  Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  *  Neither the name of Texas Instruments Incorporated nor the names of
#     its contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
#  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import queue
import time
from rtls import RTLSManager, RTLSNode

# Un-comment the below to get raw serial transaction logs
# import logging, sys
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
#                     format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')

if __name__ == '__main__':
    # Initialize, but don't start RTLS Nodes to give to the RTLSManager
    my_nodes = [RTLSNode('/dev/ttyACM0', 115200), RTLSNode('/dev/ttyACM2', 115200)]  ############## AS INSTRUCTIONS ASKED, CHANGED COM17 FOR MASTER (ACM0) AND COM12 FOR PASSIVE (ACM4)

    # Initialize references to the connected devices
    master_node = None
    passive_nodes = []
    # Initialize references to the connected devices
    address = None
    address_type = None

    # ToF related settings
    samples_per_burst = 256 # Should be dividable by 16. Hint: in a 100ms interval, there are about 300~ samples
    tof_freq_list = [2408, 2412, 2418, 2424] #Other options: 2414, 2420
    tof_num_freq = len(tof_freq_list)
    auto_tof_rssi = -55

    # Select tof_sample_mode TOF_MODE_DIST or TOF_MODE_RAW
    tof_sample_mode = 'TOF_MODE_DIST'
    tof_run_mode = 'TOF_MODE_CONT'
    seed = 0
    samplesPerFreq = 1000
    calibDistance = 1 # 1 meter
    constSyncwords = False

    # AoA related settings
    aoa_run_mode = 'AOA_MODE_ANGLE'
    aoa_cte_scan_ovs = 4
    aoa_cte_offset = 4
    aoa_cte_time = 20

    # Auto detect AoA or ToF support related
    tof_supported = False
    aoa_supported = False

    # If slave addr is None, the script will connect to the first RTLS slave
    # that it found. If you wish to connect to a specific device
    # (in the case of multiple RTLS slaves) then you may specify the address
    # explicitly as given in the comment to the right
    slave_addr = None  # '54:6C:0E:83:3F:3D'

    # Scan list
    scanResultList = list()


    # connection interval in units of 1.25msec configured in connection request, default is 80 (100ms)
    conn_interval = 80
	
    # Initialize manager reference, because on Exception we need to stop the manager to stop all the threads.
    manager = None
    try:
        # Start an RTLSManager instance without WebSocket server enabled
        manager = RTLSManager(my_nodes, websocket_port=None)
        # Create a subscriber object for RTLSManager messages
        subscriber = manager.create_subscriber()
        # Tell the manager to automatically distribute connection parameters
        manager.auto_params = True
        # Start RTLS Node threads, Serial threads, and manager thread
        manager.start()

        # Wait until nodes have responded to automatic identify command and get reference
        # to single master RTLSNode and list of passive RTLSNode instances
        master_node, passive_nodes, failed = manager.wait_identified()

        if len(failed):
            print(f"ERROR: {len(failed)} nodes could not be identified. Are they programmed?")

        # Exit if no master node exists
        if not master_node:
            raise RuntimeError("No RTLS Master node connected")

        # Combined list for lookup
        all_nodes = passive_nodes + [master_node]

        # Initialize application variables on nodes
        for node in all_nodes:
            node.tof_initialized = False
            node.seed_initialized = False
            node.aoa_initialized = False
            node.tof_calibration_configured = False
            node.tof_calibrated = False
            node.tof_started = False

        #
        # At this point the connected devices are initialized and ready
        #

        # Display list of connected devices and their capabilities
        print(f"{master_node.identifier} {', '.join([cap for cap, available in master_node.capabilities.items() if available])}")

        # Iterate over Passives and detect their capabilities
        for pn in passive_nodes:
            print(f"{pn.identifier} {', '.join([cap for cap, available in pn.capabilities.items() if available])}")

        # Check over aggregated capabilities to see if they make sense
        capabilities_per_node = [[cap for cap, avail in node.capabilities.items() if avail] for node in all_nodes]
        tof_supported = all('TOF_PASSIVE' in node_caps or 'TOF_MASTER' in node_caps for node_caps in capabilities_per_node)

        # Assume AoA if all nodes are not ToF
        aoa_supported = all(not ('TOF_PASSIVE' in node_caps or 'TOF_MASTER' in node_caps) for node_caps in capabilities_per_node)

        # Check that Nodes all must be either AoA or ToF
        if not (tof_supported or aoa_supported):
            raise RuntimeError("All nodes must be either AoA or ToF")

        # Need at least 1 passive for AoA
        if aoa_supported and len(passive_nodes) == 0:
            raise RuntimeError('Need at least 1 passive for AoA')

        # Send an example command to each of them, from commands listed at the bottom of rtls/ss_rtls.py
        for n in all_nodes:
            n.rtls.identify()

        while True:
            # Get messages from manager
            try:
                identifier, msg_pri, msg = subscriber.pend(block=True, timeout=0.05).as_tuple()

                # Get reference to RTLSNode based on identifier in message
                sending_node = manager[identifier]

                if sending_node in passive_nodes:
                    print(f"PASSIVE: {identifier} --> {msg.as_json()}")
                else:
                    print(f"MASTER: {identifier} --> {msg.as_json()}")

                # If we received an error, print it.
                if msg.command == 'RTLS_EVT_ERROR':
                    print(f"Received RTLS_EVT_ERROR with status: {msg.payload.status}")

                # If we received an assert, print it.
                if msg.command == 'RTLS_EVT_ASSERT' and msg.type == 'AsyncReq':
                    raise RuntimeError(f"Received HCI H/W Assert with code: {msg.payload.cause}")


                # After identify is received, we start scanning
                if msg.command == 'RTLS_CMD_IDENTIFY':
                    master_node.rtls.scan()

                # Once we start scaning, we will save the address of the
                # last scan response
                if msg.command == 'RTLS_CMD_SCAN' and msg.type == 'AsyncReq':
                    # Slave address none means that we connect to any slave
                    if slave_addr is None:
                        address = msg.payload.addr
                        address_type = msg.payload.addrType
                    else:
                        scanResultList.append(msg.payload.addr)
                        scanResultList.append(msg.payload.addrType)

                # Once the scan has stopped and we have a valid address, then
                # connect
                if msg.command == 'RTLS_CMD_SCAN_STOP':
                    if slave_addr is None:
                        if address is not None and address_type is not None:
                            master_node.rtls.connect(address_type, address, conn_interval)
                    elif slave_addr in scanResultList:
                        i = scanResultList.index(slave_addr)
                        master_node.rtls.connect(scanResultList[i + 1], scanResultList[i], conn_interval)
                        scanResultList.clear()
                    else:
                        # If we didn't find the device, keep scanning.
                        master_node.rtls.scan()

                # Once we are connected, then we can do stuff
                if msg.command == 'RTLS_CMD_CONNECT' and msg.type == 'AsyncReq':
                    if msg.payload.status == 'RTLS_SUCCESS':
                        if tof_supported:
                            # Find the role based on capabilities of sending node
                            role = 'TOF_MASTER' if sending_node.capabilities.get('TOF_MASTER', False) else 'TOF_PASSIVE'
                            # Send the ToF parameters to the node that just connected
                            sending_node.rtls.tof_set_params(role, samples_per_burst,
                                                             tof_num_freq, auto_tof_rssi,
                                                             tof_sample_mode, tof_run_mode,
                                                             constSyncwords, tof_freq_list)

                        if aoa_supported:
                            # Find the role based on capabilities of sending node
                            role = 'AOA_MASTER' if sending_node.capabilities.get('RTLS_MASTER', False) else 'AOA_PASSIVE'
                            # Send AoA params
                            sending_node.rtls.aoa_set_params(role, aoa_run_mode,
                                                                aoa_cte_scan_ovs,
                                                                aoa_cte_offset,
                                                                aoa_cte_time)
                    else:
                        # If the connection failed, keep scanning
                        master_node.rtls.scan()

                # Count the number of nodes that have ToF initialized
                if msg.command == 'RTLS_CMD_TOF_SET_PARAMS' and msg.payload.status == 'RTLS_SUCCESS':
                    sending_node.tof_initialized = True

                    if not passive_nodes:
                        if tof_sample_mode == 'TOF_MODE_DIST':
                            master_node.rtls.tof_calib(True, samplesPerFreq, calibDistance)
                        else:
                            # If we are not in TOF_MODE_DIST we can start immediately
                            master_node.rtls.tof_start(True)
                            master_node.tof_started = True
                    else:
                        # If all nodes have responded then we are ready to move on
                        if all([n.tof_initialized for n in all_nodes]):
                            # Send request for seed to master
                            master_node.rtls.tof_get_sec_seed()

                if msg.command == 'RTLS_CMD_AOA_SET_PARAMS' and msg.payload.status == 'RTLS_SUCCESS':
                    sending_node.aoa_initialized = True
                    if all([n.aoa_initialized for n in all_nodes]):
                        # Start AoA on the master and passive nodes
                        for node in all_nodes:
                            node.rtls.aoa_start(True)

                # Wait for security seed
                if msg.command == 'RTLS_CMD_TOF_GET_SEC_SEED' and msg.payload.seed is not 0:
                    seed = msg.payload.seed
                    for node in passive_nodes:
                        node.rtls.tof_set_sec_seed(seed)

                # Wait until passives have security seed set
                if msg.command == 'RTLS_CMD_TOF_SET_SEC_SEED' and msg.payload.status == 'RTLS_SUCCESS':
                    sending_node.seed_initialized = True

                    # Only need to calibrate in distance mode
                    if tof_sample_mode == 'TOF_MODE_DIST':
                        if sending_node in passive_nodes:
                            sending_node.tof_calibration_configured = True
                            sending_node.rtls.tof_calib(True, samplesPerFreq, calibDistance)

                        # Once all passives have calibration configured, we can configure master
                        if all([n.tof_calibration_configured for n in passive_nodes]):
                            # Master will do infinite calibration until passive is done
                            master_node.rtls.tof_calib(True, 0, calibDistance)
                    else:
                        # If we are not in TOF_MODE_DIST we can start immediately
                        if sending_node in passive_nodes:
                            sending_node.rtls.tof_start(True)
                            sending_node.tof_started = True

                        # Passives must start well before Master does since they must "hear" the first ToF exchange
                        if all([n.tof_started for n in passive_nodes]):
                            master_node.rtls.tof_start(True)
                            master_node.tof_started = True

                if msg.command == 'RTLS_CMD_TOF_CALIBRATE' and msg.type == 'SyncRsp':
                        if sending_node in passive_nodes:
                            sending_node.rtls.tof_start(True)
                            sending_node.tof_started = True

                            # Passives must start well before Master does since they must "hear" the first ToF exchange
                            if all([n.tof_started for n in passive_nodes]):
                                master_node.rtls.tof_start(True)
                                master_node.tof_started = True
                        else:
                            if not passive_nodes:
                                master_node.rtls.tof_start(True)
                                master_node.tof_started = True

                if msg.command == 'RTLS_CMD_TOF_CALIBRATE' and msg.type == 'AsyncReq':
                    if sending_node in passive_nodes:
                        sending_node.tof_calibrated = True

                        # Once all nodes are calibrated we can stop master calibration
                        if all([n.tof_calibrated for n in passive_nodes]):
                            master_node.rtls.tof_calib(False, 0, calibDistance)


            except queue.Empty:
                pass

    finally:
        if manager:
            manager.stop()
