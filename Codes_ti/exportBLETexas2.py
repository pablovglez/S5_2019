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
    mes1= AOAData()
    mes2= AOAData()
    
    try:
        #with open('/home/efisio/Documents/3Sem/S5_2019/Data/data.json') as f:
        with open('/home/efisio/Documents/3Sem/S5_2019/Data/dataBLE5.json') as f:
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
                if int(line )< 5:
                                        
                    mes1.position.append(mes.position[i])
                    mes1.distance.append(mes.distance[i])
                    mes1.time.append(mes.time[i])
                    mes1.angle.append(mes.angle[i])
                    mes1.rssi.append(mes.rssi[i])
                    mes1.antenna.append(mes.antenna[i])
                    mes1.channel.append(mes.channel[i])
                    #print(mes.distance)
                    
                else:
                    mes2.position.append(mes.position[i])
                    mes2.distance.append(mes.distance[i])
                    mes2.time.append(mes.time[i])
                    mes2.angle.append(mes.angle[i])
                    mes2.rssi.append(mes.rssi[i])
                    mes2.antenna.append(mes.antenna[i])
                    mes2.channel.append(mes.channel[i])

            #mes1.sort(key=lambda x: x.position, reverse=True)
            #pass
            #return mes1,mes2
            #print(mes.angle)    
            #print(mes2.__dict__)  
            #return mes
                
    except (Exception, psycopg2.Error) as error :
            logging.debug('Error while reading file or inserting to PostgreSQL:'.format(error))
            print ("Error while reading file or inserting to PostgreSQL", error)
    return mes1,mes2

def graph1(mes):
    print(type(mes.__dict__))
    angle_table=pd.DataFrame({'position' : mes.position,'distance' : mes.distance,'angle' : mes.angle})
    
    #sorted(mes.__dict__,key=lambda x: x.position)
    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    #print (len(mes.distance))
    print (len(mes.position))
    #print (len(mes.angle))
        
    #PLOT ANGLE VS READ POSITION
       
    #ax.plot(mes.position, mes.angle,'r+',lw=10, markersize=10)
    #angle_table.plot()
    ax.plot(angle_table['position'], angle_table['angle'],'r+',lw=10, markersize=10)

    plt.grid(True, linestyle='-', linewidth=2)
    plt.title('Position réelle vs position mesurée',loc='right',fontsize=25)
    plt.xlabel('Position réelle',fontsize=25)
    plt.ylabel('Position mesurée',fontsize=25)
    
    fig.tight_layout()
    fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/foo7.png')

def graph2(mes):

    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    print (len(mes.distance))
    print (len(mes.position))
    print (len(mes.angle))
    angle_table=pd.DataFrame({'position' : mes.position,'distance' : mes.distance,'angle' : mes.angle})
        
    #PLOT ANGLE VS READ DISTANCE 
       
    ax.boxplot(angle_table.loc[angle_table['position']=='-90']['angle'], positions=[1], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='-75']['angle'], positions=[2], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='-60']['angle'], positions=[3], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='-45']['angle'], positions=[4], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='-30']['angle'], positions=[5], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='-15']['angle'], positions=[6], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='0']['angle'], positions=[7], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='15']['angle'], positions=[8], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='30']['angle'], positions=[9], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='45']['angle'], positions=[10], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='60']['angle'], positions=[11], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='75']['angle'], positions=[12], showfliers=True)
    ax.boxplot(angle_table.loc[angle_table['position']=='90']['angle'], positions=[13], showfliers=True)
    
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13], ['-90','-75','60','-45','-30','-15','0','15','30','45','60','75','90'])
    plt.yticks([-90,-75,-60,-45,-30,-15,0,15,30,45,60,75,90])
    #plt.yticks(np.arange(-100, 100, step=10))
    
    plt.grid(True, linestyle='-', linewidth=2)
    plt.title('Position réelle vs position mesurée',loc='right',fontsize=25)
    plt.xlabel('Position réelle (en degrés)',fontsize=25)
    plt.ylabel('Position mesurée',fontsize=25)
    
    fig.tight_layout()
    fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/foo8.png')
    #fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/position_vs_mesure_bp.png')
    
def graph3(mes):
    print(len(mes.position))
    dist1=[]
    angle1=[]
    dist2=[]
    angle2=[]
    print(len(mes.distance[222]))
    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    
    for i,line in enumerate(mes.position):
        if line == '-30':
            dist1.append(mes.distance[i])
            angle1.append(mes.angle[i])
            #print(mes.distance[line])
        if line == '0':
            dist2.append(mes.distance[i])
            angle2.append(mes.angle[i])
    angle_table1=pd.DataFrame({'position' : -30,'distance' : dist1,'angle' : angle1})
    angle_table2=pd.DataFrame({'position' : -30,'distance' : dist2,'angle' : angle2})            
    #print(angle_table)
    #PLOT POSITION VS READ ANGLE 
       
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='5']['angle'], positions=[1], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='10']['angle'], positions=[2], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='15']['angle'], positions=[3], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='16']['angle'], positions=[4], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='17']['angle'], positions=[5], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='18']['angle'], positions=[6], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='19']['angle'], positions=[7], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='20']['angle'], positions=[8], showfliers=True)

    plt.xticks([1, 2,3,4,5,6,7,8], ['5','10','15','16','17','18','19','20'])
    
    plt.grid(True, linestyle='-', linewidth=2)
    plt.title('Position réelle vs position mesurée',loc='right',fontsize=25)
    plt.xlabel('Distance (en mètres)',fontsize=25)
    plt.ylabel('Position mesurée (en degrés)',fontsize=25)
    
    fig.tight_layout()
    fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/foo3.png')
    
    fig2 = plt.figure(figsize=(20,10))
    bx = plt.subplot(111)
    
    bx.boxplot(angle_table2.loc[angle_table2['distance']=='5']['angle'], positions=[1], showfliers=True)
    bx.boxplot(angle_table2.loc[angle_table2['distance']=='10']['angle'], positions=[2], showfliers=True)
    bx.boxplot(angle_table2.loc[angle_table2['distance']=='15']['angle'], positions=[3], showfliers=True)
    bx.boxplot(angle_table2.loc[angle_table2['distance']=='17']['angle'], positions=[4], showfliers=True)
    bx.boxplot(angle_table2.loc[angle_table2['distance']=='19']['angle'], positions=[5], showfliers=True)
    bx.boxplot(angle_table2.loc[angle_table2['distance']=='20']['angle'], positions=[6], showfliers=True)

    plt.xticks([1, 2,3,4,5,6], ['5','10','15','17','19','20'])
    
    plt.grid(True, linestyle='-', linewidth=2)
    plt.title('Position réelle vs position mesurée',loc='right',fontsize=25)
    plt.xlabel('Distance (en mètres)',fontsize=25)
    plt.ylabel('Position mesurée (en degrés)',fontsize=25)
    
    fig2.tight_layout()
    fig2.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/foo4.png')
    #fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/mesure_vs_distance.png')

def main():
    myList1,myList2=readData()
    #myList1=readData()
    graph1(myList2) #Use myList2 for dataBLE5 measures
    graph2(myList2) #Use myList2 for dataBLE5 measures
    #graph3(myList2)
    #print(myList1.angle)
    print('Done')
    
if __name__ == "__main__":
    main()
