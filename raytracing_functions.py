import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from math import sin, pi, inf, isnan
import pandas as pd
import sys

# Strahlinformationen in gegebener Ebene
class ynu:
    # ynu.x: absolute Distanz Objekt zu Ebene
    # ynu.y: Strahlhöhe in Ebene
    # ynu.n: Brechungsindex hinter Ebene
    # ynu.u: Steigung Strahl hinter Ebene
    def __init__(self,x = 0, y = 0, n = 0, u = 0):
        self.x = x
        self.y = y
        self.n = n
        self.u = u
    # "Schönes printen" von Klasse mit Werten
    def __repr__(self):
        return  str(self.__class__) + '\n' + '\n'.join((str(item) + ' = ' + str(self.__dict__[item]) for item in sorted(self.__dict__)))
        
# Einlesen der Datei welche optisches System beinhält
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
    
    # Tabellenheader richtig?
    if list(table.columns) != ['type', 'x', 'z', 'n', 'R']:
        print("Falsche Tabellenform!")
        print("Soll:\n['type', 'x', 'z', 'n', 'R']")
        print("Ist:\n{}".format(list(table.columns)))
        sys.exit(1)
    
    # Erste Zeile = Objekt?
    if table.type[0] != 'O':
        print('Fehler! Erste Zeile muss das Objekt (O) darstellen!')
        sys.exit(1)
    
    # Radius prüfen
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



# Berechne paraxialen Strahlengang von startPos durch table
# table: pandas Dataframe mit optischen System
# StartPos: [Index der Ebene bezogen auf table, Höhe Strahl, Steigung Strahl]
def calcYNU(table, startPos = [0, 10, 0.01]):
    startI, startY, startU = startPos
    ray = [ynu(table[:startI].x.sum(), startY, table.n[startI], startU)]
    # Durch alle Ebenen iterieren und an brechenden Ebenen neuen Strahl rechnen
    for index, surface in table.iterrows():
        # Überspringe alle Ebenen links von der Startebene
        if index < startI:
            continue
        # Überspringe Objektebene
        if surface.type == 'O':
            continue
        # Erzeuge neuen ynu-Strahl
        ray.append(ynu())
        ray[-1].x = table[:index+1].x.sum()
        ray[-1].y = ray[-2].y + ray[-2].u * surface.x
        ray[-1].n = surface.n
        # Wenn R=NaN, soll die vorige Steigung übernommen werden
        if isnan(surface.R):
            ray[-1].u = ray[-2].u
        else:
            ray[-1].u = ray[-2].n*ray[-2].u - (ray[-1].y*(ray[-1].n-ray[-2].n))/(surface.R*ray[-2].n)        
   
    return ray


# Erzeuge Plot des optischen Systems
# table: pandas Dataframe mit optischen System
# rays: [ray1, ray2, ...] mit ray=[ynu1,ynu2,...]
def plotOptSystem(table, rays):
    # Erzeuge Subplot
    fig, ax = plt.subplots()
    patches=[]
    
    # Strahlen einzeichnen als Linien zwischen Ebenen
    for ray in rays:
        for i in range(2,len(ray)+1):
            l = mlines.Line2D([ray[i-2].x,ray[i-1].x], [ray[i-2].y, ray[i-1].y])
            ax.add_line(l)     
    
    # Objekt einzeichnen
    for index, obj in table.iterrows():
       if obj.type == 'O' :
           ax.arrow(obj.x, 0, 0, obj.z-obj.z/10, head_width=4, head_length=obj.z/10, fc='k', ec='k')
    
           
    # Linsenflächen einzeichnen
    for index, surface in table.iterrows():
        if surface.type == 'L' :
            # Winkel des Bogens aus Höhe der Linse berechnen
            theta = sin(surface.z/surface.R)*180/pi
            # Winkel negieren, wenn Linse konkav
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
       
    # Achsenbegrenzungen berechnen und setzen
    # x: von min bis max mit jeweils 1/50 der Länge des opt. Systems als Rand
    # y: von min bis max mit jeweils 1/10 der maximalen Höhe als Rand
    xlim=[table.x[0]-table[:].x.sum()/50, table[:].x.sum()+table[:].x.sum()/50]
    ylim=[-1.1*table[:].z.max(), 1.1*table[:].z.max()]
    ax.set(xlim=xlim, ylim=ylim)
    
    # Optische Achse einzeichnen
    plt.plot(xlim, [0,0], color='grey', linewidth=1, linestyle='dashdot')

    # Achsenbeschriftungen setzen und plot erzeugen
    plt.xlabel('opt. Achse in mm')
    plt.ylabel('z in mm')
    plt.show




