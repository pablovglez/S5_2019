#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:47:15 2019

@author: Pablo Vinicio GONZALEZ RODRIGUEZ
@reference: rtls_example.py from Texas Instruments
"""
import argparse
import json
import queue
import time
from rtls import RTLSManager, RTLSNode
import multiprocessing

# Un-comment the below to get raw serial transaction logs
# import logging, sys
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
#                     format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')

# Un-comment the below to get raw serial transaction logs
# import logging, sys
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
#                     format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')

master_node = None
passive_nodes= []
address = None
address_type = None
timestamp = 0

parser = argparse.ArgumentParser(description='Returns the distance between the passive and the slave. ' +
    'Returns the position of the slave relative to the passive. ' +
    'Example:    test.py \'distance\' , \'position\' and \'duration\'\''+
    'These samples were taken using Python\'')
parser.add_argument("distance", help="Displays distance between the passive and the slave")
parser.add_argument("position", help="Displays angle between the passive and the slave")
parser.add_argument("duration", help="Test duration in minutes")
args = parser.parse_args()

def run_forever():
    # Initialize, but don't start RTLS Nodes to give to the RTLSManager
    my_nodes = [RTLSNode('/dev/ttyACM0', 115200), RTLSNode('/dev/ttyACM2', 115200)]

    # Initialize references to the connected devices
    master_node = None
    passive_nodes = []
    # Initialize references to the connected devices
    address = None
    address_type = None

    # AoA related settings
    aoa_run_mode = 'AOA_MODE_ANGLE'
    aoa_cte_scan_ovs = 4
    aoa_cte_offset = 4
    aoa_cte_time = 20

    # Auto detect AoA or ToF support related
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
            node.seed_initialized = False
            node.aoa_initialized = False

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

        # Assume AoA if all nodes are not ToF
        aoa_supported = all(not ('TOF_PASSIVE' in node_caps or 'TOF_MASTER' in node_caps) for node_caps in capabilities_per_node)

        # Check that Nodes all must be AoA
        if not (aoa_supported):
            raise RuntimeError("All nodes must be AoA")

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

                try:
                    with open("Output/test.json","a") as fichier:
                        message=json.loads("["+msg.as_json()+"]")
                        message[0]["payload"]["time"]=timestamp
                        message[0]["payload"]["distance"]=args.distance
                        message[0]["payload"]["position"]=args.position
                        json.dump(message[0]["payload"], fichier)
                        print(message[0]["payload"])
                        fichier.write('\n')
                        fichier.close
                except:
                    print ('\nProblem writing on JSON file')
                    break

            except queue.Empty:
                pass

    finally:
        if manager:
            manager.stop()

if __name__ == '__main__':
    #Start RTLS as a process
    p=multiprocessing.Process(target=run_forever, name="Run_Forever")
    p.start()

    #Wait "t" minutes
    time.sleep(60*int(args.duration))

    #Terminate RTLS
    p.terminate()
    print("\n\n RTLS AoA scan stopped after "+args.duration+" minutes \n")

    p.join()
