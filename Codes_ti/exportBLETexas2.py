import json
import psycopg2
import logging #Provides a logging system
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

def readData():
    mes= AOAData()
    mes1= AOAData()
    mes2= AOAData()
    
    try:
        #with open('/home/efisio/Documents/3Sem/S5_2019/Data/data.json') as f:
        with open('/home/efisio/Documents/3Sem/S5_2019/Data/dataBLE9.json') as f:
            mes.distance=[]  
            mes1.distance=[]  
            mes1.position=[]
            mes1.angle=[]
            mes2.distance=[]
            mes2.position=[]
            mes2.angle=[]
            
            #READ THE RAW DATA 

            for entry in f:                
                dict = json.loads(entry)
                mes.position.append(dict.get('position', 0))
                mes.distance.append(dict.get('distance', 0))
                mes.time.append(dict.get('time', 0))
                mes.angle.append(dict.get('angle', 0))
                mes.rssi.append(dict.get('rssi', 0))
                mes.antenna.append(dict.get('antenna', 0))
                mes.channel.append(dict.get('channel', 0))
                #myList.append(mes.__dict__)
                
            #SEPARATE THE RANGE TESTS (BELOW 5 METERS) FROM THE REGULAR TESTS
            
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

    except (Exception, psycopg2.Error) as error :
            logging.debug('Error while reading file or inserting to PostgreSQL:'.format(error))
            print ("Error while reading file or inserting to PostgreSQL", error)
    return mes1,mes2

def pointed_graph(mes):
    angle_table=pd.DataFrame({'position' : mes.position,'distance' : mes.distance,'angle' : mes.angle})
    
    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    
    #PLOT ANGLE VS READ POSITION
       
    ax.plot(angle_table['position'], angle_table['angle'],'r+',lw=10, markersize=10)

    plt.grid(True, linestyle='-', linewidth=2)
    plt.title('Position réelle vs position mesurée',loc='right',fontsize=25)
    plt.xlabel('Position réelle',fontsize=25)
    plt.ylabel('Position mesurée',fontsize=25)
    
    fig.tight_layout()
    fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/position_vs_mesure_pt.png')

def boxplot_graphs(mes):

    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    print (len(mes.distance))
    print (len(mes.position))
    print (len(mes.angle))
    angle_table=pd.DataFrame({'position' : mes.position,'distance' : mes.distance,'angle' : mes.angle})
       
    ax.boxplot(angle_table.loc[angle_table['position']=='-90']['angle'], positions=[1], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='-75']['angle'], positions=[2], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='-60']['angle'], positions=[3], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='-45']['angle'], positions=[4], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='-30']['angle'], positions=[5], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='-15']['angle'], positions=[6], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='0']['angle'], positions=[7], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='15']['angle'], positions=[8], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='30']['angle'], positions=[9], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='45']['angle'], positions=[10], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='60']['angle'], positions=[11], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='75']['angle'], positions=[12], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    ax.boxplot(angle_table.loc[angle_table['position']=='90']['angle'], positions=[13], showfliers=True,boxprops= dict(linewidth=2.0, color='black'), whiskerprops=dict(linestyle='-',linewidth=2.0, color='black'), medianprops=dict(linestyle='-',linewidth=2.0, color='r'))
    
    ax.tick_params(direction='out', length=6, width=2, grid_alpha=0.5)
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13], ['-90','-75','-60','-45','-30','-15','0','15','30','45','60','75','90'])
    plt.yticks([-90,-75,-60,-45,-30,-15,0,15,30,45,60,75,90])
    
    plt.grid(True, linestyle='-', linewidth=2)
    #plt.title('Position réelle vs position mesurée',loc='right',fontsize=25)
    #plt.xlabel('Position réelle (en degrés)',fontsize=25)
    #plt.ylabel('Position mesurée',fontsize=25)
    
    fig.tight_layout()
    fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/position_vs_mesure_bp.png')
    
def range_graph(mes):
    dist1=[]
    angle1=[]
    dist2=[]
    angle2=[]
    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    
    for i,line in enumerate(mes.position):
        if line == '-30':
            dist1.append(mes.distance[i])
            angle1.append(mes.angle[i])
        if line == '0':
            dist2.append(mes.distance[i])
            angle2.append(mes.angle[i])
    angle_table1=pd.DataFrame({'position' : -30,'distance' : dist1,'angle' : angle1})
    angle_table2=pd.DataFrame({'position' : 0,'distance' : dist2,'angle' : angle2})            
       
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='5']['angle'], positions=[1], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='10']['angle'], positions=[2], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='15']['angle'], positions=[3], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='16']['angle'], positions=[4], showfliers=True)
    #ax.boxplot(angle_table1.loc[angle_table1['distance']=='17']['angle'], positions=[5], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='18']['angle'], positions=[5], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='19']['angle'], positions=[6], showfliers=True)
    ax.boxplot(angle_table1.loc[angle_table1['distance']=='20']['angle'], positions=[7], showfliers=True)

    plt.xticks([1, 2,3,4,5,6,7], ['5','10','15','16','18','19','20'])
    
    plt.grid(True, linestyle='-', linewidth=2)
    plt.title('Position mesurée vs distance (à -30 degrées)',loc='right',fontsize=25)
    plt.xlabel('Distance (en mètres)',fontsize=25)
    plt.ylabel('Position mesurée (en degrés)',fontsize=25)
    
    fig.tight_layout()
    fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/mesure_vs_distance_30d.png')
    
    fig2 = plt.figure(figsize=(20,10))
    bx = plt.subplot(111)
    
    bx.boxplot(angle_table2.loc[angle_table2['distance']=='5']['angle'], positions=[1], showfliers=True)
    bx.boxplot(angle_table2.loc[angle_table2['distance']=='10']['angle'], positions=[2], showfliers=True)
    bx.boxplot(angle_table2.loc[angle_table2['distance']=='15']['angle'], positions=[3], showfliers=True)
    bx.boxplot(angle_table2.loc[angle_table2['distance']=='17']['angle'], positions=[4], showfliers=True)
    bx.boxplot(angle_table2.loc[angle_table2['distance']=='19']['angle'], positions=[5], showfliers=True)

    plt.xticks([1, 2,3,4,5], ['5','10','15','17','19'])
    
    plt.grid(True, linestyle='-', linewidth=2)
    plt.title('Position mesurée vs distance (à 0 degrées)',loc='right',fontsize=25)
    plt.xlabel('Distance (en mètres)',fontsize=25)
    plt.ylabel('Position mesurée (en degrés)',fontsize=25)
    
    fig2.tight_layout()
    fig2.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/mesure_vs_distance_0d.png')
        
def path_graph(mes,path):
    mes.time=mes.time[0:len(mes.angle)]
    times=[ float(x)-float(mes.time[1]) for x in mes.time ] #used to normalize the time vector
    
    
    angle_table=pd.DataFrame({'time' : times,'distance' : mes.distance,'angle' : mes.angle}).sort_values(by=['time'],ascending=True)
    angle_table=pd.DataFrame({'time' : angle_table.loc[angle_table['distance']==path]['time']-angle_table.loc[angle_table['distance']==path]['time'].iloc[1],'distance' : angle_table.loc[angle_table['distance']==path]['distance'],'angle' : angle_table.loc[angle_table['distance']==path]['angle']}).sort_values(by=['time'],ascending=True)
        
    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    plt.title('Position mesurée vs temps',loc='right',fontsize=25)
    plt.xlabel('Temps (secondes)',fontsize=25)
    plt.ylabel('Position mesurée (en degrées)',fontsize=25)
    angle_table.plot()
    ax.plot(angle_table['time'], angle_table['angle'],'r+',lw=10, markersize=10)
    ax.grid(True, linestyle='-', linewidth=2)
       
    fig.tight_layout()
    fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/mesure_vs_temps_pt_'+path+'.png')
    
def get_sem(mes,test):
    fig = plt.figure(figsize=(20,10))
    cx = plt.subplot(111)
    print (len(mes.distance))
    print (len(mes.position))
    print (len(mes.angle))
    angle_table=pd.DataFrame({'position' : mes.position,'distance' : mes.distance,'angle' : mes.angle})
    errors=[]

    for i in range(0,14):
        errors.extend([angle_table.loc[angle_table['position']==str(-90+(15*(i)))]['angle'].sem(axis=0)]) #Calculate de variance of the observed angle
 
    cx.errorbar(angle_table.loc[angle_table['position']=='-90']['position'], angle_table.loc[angle_table['position']=='-90']['angle'], errors[1],linewidth=4.0,color='orange',barsabove=True)
    cx.errorbar(angle_table.loc[angle_table['position']=='-75']['position'], angle_table.loc[angle_table['position']=='-75']['angle'], errors[2],linewidth=4.0,color='orange')
    cx.errorbar(angle_table.loc[angle_table['position']=='-60']['position'], angle_table.loc[angle_table['position']=='-60']['angle'], errors[3],linewidth=4.0,color='orange')
    cx.errorbar(angle_table.loc[angle_table['position']=='-45']['position'], angle_table.loc[angle_table['position']=='-45']['angle'], errors[4],linewidth=4.0,color='orange')
    cx.errorbar(angle_table.loc[angle_table['position']=='-30']['position'], angle_table.loc[angle_table['position']=='-30']['angle'], errors[5],linewidth=4.0,color='orange')
    cx.errorbar(angle_table.loc[angle_table['position']=='-15']['position'], angle_table.loc[angle_table['position']=='-15']['angle'], errors[6],linewidth=4.0,color='orange')
    cx.errorbar(angle_table.loc[angle_table['position']=='0']['position'], angle_table.loc[angle_table['position']=='0']['angle'], errors[7],linewidth=4.0,color='orange')
    cx.errorbar(angle_table.loc[angle_table['position']=='15']['position'], angle_table.loc[angle_table['position']=='15']['angle'], errors[8],linewidth=4.0,color='orange')
    cx.errorbar(angle_table.loc[angle_table['position']=='30']['position'], angle_table.loc[angle_table['position']=='30']['angle'], errors[9],linewidth=4.0,color='orange')
    cx.errorbar(angle_table.loc[angle_table['position']=='45']['position'], angle_table.loc[angle_table['position']=='45']['angle'], errors[10],linewidth=4.0,color='orange')
    cx.errorbar(angle_table.loc[angle_table['position']=='60']['position'], angle_table.loc[angle_table['position']=='60']['angle'], errors[11],linewidth=4.0,color='orange')
    cx.errorbar(angle_table.loc[angle_table['position']=='75']['position'], angle_table.loc[angle_table['position']=='75']['angle'], errors[12],linewidth=4.0,color='orange')
    cx.errorbar(angle_table.loc[angle_table['position']=='90']['position'], angle_table.loc[angle_table['position']=='90']['angle'], errors[13],linewidth=4.0,color='orange')
    
    cx.tick_params(direction='out', length=6, width=2, grid_alpha=0.5)
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13], ['-90','-75','-60','-45','-30','-15','0','15','30','45','60','75','90'])
    plt.yticks([-90,-75,-60,-45,-30,-15,0,15,30,45,60,75,90])
    
    plt.grid(True, linestyle='-', linewidth=2)
    
    fig.tight_layout()
    fig.savefig('//home/efisio/Documents/3Sem/S5_2019/Data/errors_test_'+test+'.png')
    print ("|  Position\t  |\t Error     |")
    print ("____________________________________")
    for i in range(0,13):
        print (str(-90+(15*(i)))+"\t"+"%.5f"% errors[i])
        #print ("|"+str(-90+(15*(i)))+"\t\t  |\t "+"%.5f"% errors[i]+ "   |" )

def main():
    myList1,myList2=readData()
    #pointed_graph(myList1) #Use myList2 for dataBLE5 measures
    #boxplot_graphs(myList1) #Use myList2 for dataBLE5 measures
    get_sem(myList1,'9') #Use myList2 for dataBLE5 measures
    #range_graph(myList1,'4') #Use myList2 for dataBLE5 measures
    #print(myList1.angle)
    print('Done')
    
if __name__ == "__main__":
    main()