#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:47:15 2019

@author: efisio
"""

import argparse
import queue
import json
import time
from rtls import RTLSManager, RTLSNode

master_node = None
passive_nodes= []
address = None
address_type = None
timestamp = 0

parser = argparse.ArgumentParser(description='Returns the distance between the passive and the slave. ' +
    'Returns the position of the slave relative to the passive. ' +
    'Example:    test.py \'distance\' and \'position\' \''+
    'These samples were taken using Python\'')
parser.add_argument("distance", help="Displays distance")
parser.add_argument("position", help="Displays time")
args = parser.parse_args()

#First, construct an instance of the RTLSNode class for the master and passive
#device connected to PC. The first parameter is the user/UART COM port, and 
#the second is the baudrate which defaults to 115200

my_nodes = [RTLSNode('/dev/ttyACM4', 115200), RTLSNode('/dev/ttyACM2', 115200)]

#Instantiate the RTLSManager will the newly created nodes, 
#but do not connect a rtls_agent_cli.

try:
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
            identifier, msg_pri, msg = subscriber.pend(block=True, timeout=0.05).as_tuple() #PVGR MSG COMMES FROM SUBSCRIBER?
    
            # Pend on activity from one of the nodes with a given timeout.
    
            # We received data from one of the nodes
            # First determine which node sent the information.
            from_node = master_node.identifier
            # Get reference to RTLSNode based on identifier in message
            sending_node = manager[identifier]
            # Print the message as JSON, map MASTER and PASSIVE based on identifier (BD_ADDR)
            #if sending_node in passive_nodes:
                #pass
                #print(f"PASSIVE: {identifier} --> {msg.as_json()}")
            #else:
                #print(f"MASTER: {identifier} --> {msg.as_json()}")
    
            # Perform further processing here.
            if msg.command == 'RTLS_CMD_IDENTIFY':
                master_node.rtls.scan()
            if msg.command == 'RTLS_CMD_SCAN' and msg.type == 'AsyncReq':
                address = msg.payload.addr
                address_type = msg.payload.addrType
            timestamp = time.time()
            try:
                with open("/home/efisio/ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent/examples/data.json","a") as fichier:
                    message=json.loads("["+msg.as_json()+"]")
                    message[0]["payload"]["time"]=timestamp
                    message[0]["payload"]["distance"]=args.distance
                    message[0]["payload"]["position"]=args.position
                    #message[0]["payload"]["address"]=address #AT THIS TIME IS NOT KNOWN NOR NECESSARY
                    json.dump(message[0]["payload"], fichier)
                    print(message[0]["payload"])
                    fichier.write('\n')
                    fichier.close
            except:
                print ('\nProblem writing on JSON file')
                break
                    
        except queue.Empty:
            pass
        except (KeyboardInterrupt, SystemExit):
            print ('\nkeyboardinterrupt caught (again)')
            print ('\n...Program Stopped Manually!')
            break

except:
    raise