#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:47:15 2019

@author: efisio
"""

import queue
from rtls import RTLSManager, RTLSNode

#First, construct an instance of the RTLSNode class for the master and passive
#device connected to PC. The first parameter is the user/UART COM port, and 
#the second is the baudrate which defaults to 115200

my_nodes = [RTLSNode('/dev/ttyACM0', 115200), RTLSNode('/dev/ttyACM4', 115200)]

#Instantiate the RTLSManager will the newly created nodes, 
#but do not connect a rtls_agent_cli.

manager = RTLSManager(my_nodes, websocket_port=None)

#Create a subscriber instance, and add it to the manager. Essentially this 
#tells the manager to add messages it receives to the example programs queue 
#to be processed. Tell the manager to automatically distribute connection 
#parameters to all of the passive nodes. Then start the manager.

subscriber = manager.create_subscriber()
# Tell the manager to automatically distribute connection parameters
manager.auto_params = True
# Start RTLS Node threads, Serial threads, and manager thread
manager.start()

#Poll the capabilities of each node, assign master and create list of passives.

# Wait until nodes have responded to automatic identify command and get reference
# to single master RTLSNode and list of passive RTLSNode instances
master_node, passive_nodes, failed = manager.wait_identified()

#Now that we have instantiated the classes, and got the capabilities of the
# nodes, we are ready to create the main loop.

while True:
    # Get messages from manager
    try:
        # Pend on activity from one of the nodes with a given timeout.
        identifier, msg_pri, msg = subscriber.pend(block=True, timeout=0.05).as_tuple()

        # We received data from one of the nodes
        # First determine which node sent the information.
        from_node = node_msg.identifier

        # Print the message as JSON, map MASTER and PASSIVE based on identifier (BD_ADDR)
        if sending_node in passive_nodes:
            print(f"PASSIVE: {identifier} --> {msg.as_json()}")
        else:
            print(f"MASTER: {identifier} --> {msg.as_json()}")

        # Perform further processing here.

    except queue.Empty:
        pass

