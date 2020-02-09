#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 11:37:00 2020

@author: efisio
"""

import json
import psycopg2
import logging #Provides a logging system
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 20

class AOAData():
    position=[] #Actual angle where the slave is placed (which mark on the ground)
    distance=[] #Distance from the passive to slave
    time=[] 
    angle=[] #Measured angle (by the passive)
    rssi=[]
    antenna=[]
    channel=[]

def myFunc(e):
  return e   

def readData():
    mes= AOAData()
    
    """try:
        #with open('/home/efisio/Documents/3Sem/S5_2019/Data/data.json') as f:
        with open('/home/efisio/Documents/3Sem/S5_2019/Data/copy.json') as f:
            for entry in f:                
                dict = json.loads(entry)

                mes.position.append(dict.get('position', 0))
                mes.distance.append(dict.get('distance', 0))
                mes.time.append(dict.get('time', 0))
                mes.angle.append(dict.get('angle', 0))
                mes.rssi.append(dict.get('rssi', 0))
                mes.antenna.append(dict.get('antenna', 0))
                mes.channel.append(dict.get('channel', 0))"""
                
    try:
        #with open('/home/efisio/Documents/3Sem/S5_2019/Data/data.json') as f:
        with open('/home/efisio/Documents/3Sem/S5_2019/Data/dataBLE.json') as f:
            mes.distance=[]
            for entry in f:                
                dict = json.loads(entry)
                mes.position.append(dict.get('position', 0))
                mes.distance.append(dict.get('distance', 0))
                mes.time.append(dict.get('time', 0))
                mes.angle.append(dict.get('angle', 0))
                mes.rssi.append(dict.get('rssi', 0))
                mes.antenna.append(dict.get('antenna', 0))
                mes.channel.append(dict.get('channel', 0))

        
    except (Exception, psycopg2.Error) as error :
            logging.debug('Error while reading file'.format(error))
            print ("Error while reading file", error)
    try:
        print(type(mes.time[1]))
        print((mes.time[1]))    
        with open("/home/efisio/Documents/3Sem/S5_2019/Data/test.json","a") as fichier2:
            
            for i, line in enumerate(mes.time):
                fichier2.write('{"')
                fichier2.write('position": ')
                fichier2.write(str(mes.position[i]))
                fichier2.write(', "')
                fichier2.write('distance": ')
                fichier2.write(str(mes.distance[i]))
                fichier2.write(', "')
                fichier2.write('time": ')
                fichier2.write(str(mes.time[i]))
                fichier2.write(', "')
                fichier2.write('angle": ')
                fichier2.write(str(mes.angle[i])) 
                fichier2.write(', "')
                fichier2.write('rssi": ')
                fichier2.write(str(mes.rssi[i])) 
                fichier2.write(', "')
                fichier2.write('antenna": ')
                fichier2.write(str(mes.antenna[i])) 
                fichier2.write(', "')
                fichier2.write('channel": ')
                fichier2.write(str(mes.channel[i]))
                 
                #fichier2.write('" "')
                
                fichier2.write('}\n')
                """ang=json.dumps(mes.angle)
                rss=json.dumps(mes.rssi)
                ant=json.dumps(mes.antenna)
                cha=json.dumps(mes.channel)
                tim=json.dumps(line)
                dis=json.dumps(mes.distance)
                pos=json.dumps(mes.position)
                #arr=json.dumps(line)
                print(ang[i])
                
                #print(mes["time"])
                #message[0]["payload"]["address"]=address #AT THIS TIME IS NOT KNOWN NOR NECESSARY
                json.dump(cha, fichier2)
                #print(message[0]["payload"])"""
            fichier2.write('\n')
            fichier2.close
        
    except (Exception, psycopg2.Error) as error :
            logging.debug('Error while saving new file:'.format(error))
            print ("Error while saving new file: ", error)
    
    f.close
    return mes

def main():
    myList1=readData()
    #print(myList1.angle)
    print('Done')
    
if __name__ == "__main__":
    main()