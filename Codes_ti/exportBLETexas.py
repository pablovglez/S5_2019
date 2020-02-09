import json
import psycopg2
import logging #Provides a logging system
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 20

class AOAData():
    position=[]
    distance=[]
    time=[]
    angle=[]
    rssi=[]
    antenna=[]
    channel=[]

def readData():
    mes= AOAData()
    mes1= AOAData()
    mes2= AOAData()
    try:
        #with open('/home/efisio/Documents/3Sem/S5_2019/Data/data.json') as f:
        with open('/home/efisio/Documents/3Sem/S5_2019/Data/dataBLE.json') as f:
            mes.distance=[]
            mes1.distance=[]
            mes1.position=[]
            mes1.angle=[]
            mes2.distance=[]
            mes2.position=[]
            mes2.angle=[]
            for entry in f:                
                dict = json.loads(entry)
                #if dict['class']=='SKY':
                #mes.position=30
                """mes.position=dict.get('position', 0)
                #mes.distance=20
                mes.distance=dict.get('distance', 0)
                mes.time=dict.get('time', 0)
                mes.angle=dict.get('angle', 0)
                mes.rssi=dict.get('rssi', 0)
                mes.antenna=dict.get('antenna', 0)
                mes.channel=dict.get('channel', 0)"""
                """with open('/home/efisio/Documents/3Sem/S5_2019/Data/dataBLE.json',"a") as fichier2:
                    #print(type(mes.__dict__))
                    json.dump(mes.__dict__, fichier2)
                    fichier2.write('\n')
                    fichier2.close"""
                                #print(test)
                mes.position.append(dict.get('position', 0))
                mes.distance.append(dict.get('distance', 0))
                mes.time.append(dict.get('time', 0))
                mes.angle.append(dict.get('angle', 0))
                mes.rssi.append(dict.get('rssi', 0))
                mes.antenna.append(dict.get('antenna', 0))
                mes.channel.append(dict.get('channel', 0))
                #myList.append(mes.__dict__)

            for i, line in enumerate(mes.distance):
                if line < 6:

                    mes1.position.append(mes.position[i])
                    mes1.distance.append(mes.distance[i])
                    mes1.time.append(mes.time[i])
                    mes1.angle.append(mes.angle[i])
                    mes1.rssi.append(mes.rssi[i])
                    mes1.antenna.append(mes.antenna[i])
                    mes1.channel.append(mes.channel[i])
            for i, line in enumerate(mes.position):
                if line == 30:

                    mes2.position.append(mes.position[i-1])
                    mes2.distance.append(mes.distance[i-1])
                    mes2.time.append(mes.time[i-1])
                    mes2.angle.append(mes.angle[i-1])
                    mes2.rssi.append(mes.rssi[i])
                    mes2.antenna.append(mes.antenna[i-1])
                    mes2.channel.append(mes.channel[i-1])
                    #pass
            return mes1,mes2

    except (Exception, psycopg2.Error) as error :
            logging.debug('Error while reading file or inserting to PostgreSQL:'.format(error))
            print ("Error while reading file or inserting to PostgreSQL", error)

def graph1(mes):

    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    print (len(mes.distance))
    print (len(mes.position))
    print (len(mes.angle))

    #PLOT ANGLE VS READ POSITION

    ax.plot(mes.position, mes.angle,'r+',lw=10, markersize=10)

    plt.grid(True, linestyle='-', linewidth=2)
    plt.title('Position réelle vs position mesurée (points)',loc='right',fontsize=25)
    plt.xlabel('Position réelle (en degrés)',fontsize=25)
    plt.ylabel('Position mesurée (en degrés)',fontsize=25)
    plt.xticks([0,30,60,90])

    fig.tight_layout()
    fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/position_vs_mesure_pt.png')

def graph2(mes):

    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    print (len(mes.distance))
    print (len(mes.position))
    print (len(mes.angle))
    angle_table=pd.DataFrame({'position' : mes.position,'distance' : mes.distance,'angle' : mes.angle})

    #PLOT ANGLE VS READ DISTANCE 

    ax.boxplot(angle_table.loc[angle_table['position']==0]['angle'], positions=[1], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']==30]['angle'], positions=[2], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']==60]['angle'], positions=[3], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']==90]['angle'], positions=[4], showfliers=True)
    plt.xticks([1, 2,3,4], ['0','30','60','90'])

    plt.grid(True, linestyle='-', linewidth=2)
    plt.title('Position réelle vs position mesurée (boxplot)',loc='right',fontsize=25)
    plt.xlabel('Position réelle (en degrés)',fontsize=25)
    plt.ylabel('Position mesurée (en degrés)',fontsize=25)

    fig.tight_layout()
    fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/position_vs_mesure_bp.png')

def graph3(mes):

    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    angle_table=pd.DataFrame({'position' : mes.position,'distance' : mes.distance,'angle' : mes.angle})

    #PLOT POSITION VS READ ANGLE 

    ax.boxplot(angle_table.loc[angle_table['distance']==1]['angle'], positions=[1], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['distance']==2]['angle'], positions=[2], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['distance']==3]['angle'], positions=[3], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['distance']==4]['angle'], positions=[4], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['distance']==5]['angle'], positions=[5], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['distance']==8]['angle'], positions=[6], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['distance']==10]['angle'], positions=[7], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['distance']==15]['angle'], positions=[8], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['distance']==19]['angle'], positions=[9], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['distance']==20]['angle'], positions=[10], showfliers=True)
    plt.xticks([1, 2,3,4,5,6,7,8,9,10], ['1','2','3','4','5','8','10','15','19','20'])

    plt.grid(True, linestyle='-', linewidth=2)
    plt.title('Position réelle vs position mesurée (boxplot)',loc='right',fontsize=25)
    plt.xlabel('Distance (en mètres)',fontsize=25)
    plt.ylabel('Position mesurée (en degrés)',fontsize=25)

    fig.tight_layout()
    fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/mesure_vs_distance.png')

def main():
    myList1,myList2=readData()
    graph1(myList1)
    graph2(myList1)
    graph3(myList2)
    #print(myList1.angle)
    print('Done')

if __name__ == "__main__":
    main()