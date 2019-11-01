import pandas as pd
import sys

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from math import sin, pi, inf, isnan


class ynu:
    def __init__(self,x = 0, y = 0, n = 0, u = 0):
        self.x = x
        self.y = y
        self.n = n
        self.u = u
    def __repr__(self):
        return  str(self.__class__) + '\n' + '\n'.join((str(item) + ' = ' + str(self.__dict__[item]) for item in sorted(self.__dict__)))
        
# Einlesen der Datei inkl. Fehlerausgabe
def loadOptSystem(fileName):
    try:
        table = pd.read_csv(fileName, sep = '\t')
    except IndexError:
        print("Error! Datei mit Linsensystem nicht als Parameter angegeben!")
        sys.exit(1)
    except FileNotFoundError:
        print("Error! Datei \"{}\" konnte nicht gefunden werden".format(sys.argv[1]))
        sys.exit(1)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
        exit
    
    if table.type[0] != 'O':
        print('Fehler! Erste Zeile muss das Objekt (O) darstellen!')
        sys.exit(1)
        
    for i in range(len(table)):
        if table.R[i] == 0:
            print('Fehler! Radius darf nicht 0 sein')
            sys.exit(1) 
        if table.R[i] == 'infty':
            table.R[i] = inf
    
        
        
    return table

# Tausche alle Ebenen außer Objekt (index=0)
def invertTable(table):
#    print('Unbearbeitet:\n',table)
    
    # Objekt rausnehmen
    obj = table.loc[0]
    table = table.drop(0)
#    print('Obj dropped:\n', table)    
    
    # Umdrehen aller Ebenen
    for i in range(1,len(table)//2+1):
        table.loc[i], table.loc[len(table)-i+1] = table.loc[len(table)-i+1], table.loc[i]
    
#    print('Neu sortiert:\n', table)
    
    # Tauschen der rel. X-Positionen
    for i in range(1,len(table)):
        #print('Ich tausche {} und {}'.format(i, i-1))
        if i == 1:
            table.loc[len(table),'x'], table.loc[i,'x'] = table.loc[i,'x'], table.loc[len(table),'x']
            table.loc[len(table),'n'], table.loc[i,'n'] = table.loc[i,'n'], table.loc[len(table),'n']
        else:
            table.loc[i+1,'x'], table.loc[i,'x'] = table.loc[i,'x'], table.loc[i+1,'x']
            table.loc[i+1,'n'], table.loc[i,'n'] = table.loc[i,'n'], table.loc[i+1,'n']

#        print(table)
            
    # Radien + -> -, - -> +
    for i in range(1,len(table)+1):
        print('Row:\n',table.loc[i])
        if table.loc[i, 'R']:
            print('in if')
            table.loc[i, 'R'] = -table.loc[i, 'R']
        print('Row ggf bearbeitet:\n', table.loc[i, 'R'])
        
        
    # Objekt einfügen
    table.loc[0]=obj
    table = table.sort_index()
    
#    print('Fertig:\n', table)
    return table




def calcYNU(table, startPos = [0, 10, 0.01]):
    startI, startY, startU = startPos
    strahl = [ynu(table[:startI].x.sum(), startY, table.n[startI], startU)]
    for index, surface in table.iterrows():
        if index < startI:
            continue
        if surface.type == 'O':
            continue
        strahl.append(ynu())
        strahl[-1].x = table[:index+1].x.sum()
        strahl[-1].y = strahl[-2].y + strahl[-2].u * surface.x
        strahl[-1].n = surface.n
        if isnan(surface.R):
            strahl[-1].u = strahl[-2].u
        else:
            strahl[-1].u = strahl[-2].n*strahl[-2].u - (strahl[-1].y*(strahl[-1].n-strahl[-2].n))/(surface.R*strahl[-2].n)        
   
    return strahl



def plotOptSystem(strahl, table):
    fig, ax = plt.subplots()
    patches=[]
    for i in range(2,len(strahl)+1):
        l = mlines.Line2D([strahl[i-2].x,strahl[i-1].x], [strahl[i-2].y, strahl[i-1].y])
        ax.add_line(l)     
    
    # Objekt einzeichnen
    for index, obj in table.iterrows():
       if obj.type == 'O' :
           ax.arrow(obj.x, 0, 0, obj.z-obj.z/10, head_width=4, head_length=obj.z/10, fc='k', ec='k')
    
           
    # Linsenflächen einzeichnen
    for index, surface in table.iterrows():
        if surface.type == 'L' :
            theta = sin(surface.z/surface.R)*180/pi
            if surface.R < 0:
                theta = -theta
            arc = Arc((table[:index+1].x.sum()+surface.R, 0), 2*surface.R, 2*surface.R, 0, -theta-180, theta-180, edgecolor ='b', facecolor ='none')
            patches.append(arc)
            ax.add_artist(arc)
    
    
    # Stop Einzeichnen
    for index, stop in table.iterrows():
      if stop.type == 'S' :
          ax.vlines(table[:index+1].x.sum(), stop.z, table[:index+1].z.sum(), colors='r', linestyles='solid', label='') 
          ax.vlines(table[:index+1].x.sum(), -stop.z, -table[:index+1].z.sum(), colors='r', linestyles='solid', label='') 
     
    # Mirror einzeichnen
    
    
    
    
    xlim=[table.x[0]-table[:].x.sum()/50, table[:].x.sum()+table[:].x.sum()/50]
    ylim=[-1.1*table[:].z.max(), 1.1*table[:].z.max()]
    ax.set(xlim=xlim, ylim=ylim)
    #ax.set(xlim=[290, 350], ylim=[-15, 15])#einfach auskommentieren
    #ax.set(xlim=[350, 600], ylim=[-50, 50])
    
    plt.xlabel('opt. Achse in mm')
    plt.ylabel('z in mm')
    plt.plot(xlim, [0,0], color='grey', linewidth=1, linestyle='dashdot')
    plt.show




