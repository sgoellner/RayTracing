import matplotlib.lines as mlines
import matplotlib.pyplot as plt
#import raytracing_gui as gui
import os
from tkinter.filedialog import askopenfilename 
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
        return  (str(self.__class__) + '\n' + 
                 '\n'.join((str(item) + ' = ' + str(self.__dict__[item])
                            for item in sorted(self.__dict__))))
        
        

        
# Einlesen der Datei welche optisches System beinhält
def loadOptSystem():
    try:
        table = pd.read_csv(askopenfilename(initialdir = os.getcwd(), filetypes =[('Text Files', '*.txt'), ("all files","*.*")]), sep = '\t')
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



# Berechne paraxialen Strahlengang von startPos durch table
# table: pandas Dataframe mit optischen System
# StartPos: [Index der Ebene bezogen auf table, Höhe Strahl, Steigung Strahl]
def calcYNU(table, startPos = [0, 10, 0.01], inverted=False):
    startI, startY, startU = startPos
    ray = [ynu(
            table[:startI+1].x.sum(),
            startY, 
            table.n[startI], 
            startU)
    ]
    # Durch alle Ebenen iterieren und an brechenden Ebenen neuen Strahl rechnen
    
    i = startI
    while True:
        # Hoch/Runterzählen des Indexes
        i += 1 if not inverted else -1
        # Schleife beenden wenn Index aus table rausgelaufen ist
        if(i < 0 or i >= len(table)): break
        # Erzeuge neuen ynu-Strahl
        ray.append(ynu())
        # x ist der Abstand zum Objekt
        ray[-1].x = table[:i+1].x.sum()
        # Transfergleichung
        # y' = y + ud
        ray[-1].y = ray[-2].y + ray[-2].u * (
                table.loc[i].x if not inverted else table.loc[i+1].x)
        ray[-1].n = table.loc[i].n if(not inverted or i == 0) else table.loc[i-1].n
        # Wenn R=NaN, soll die vorige Steigung übernommen werden
        # sonst: n'u' = nu-y(n'-n)/R
        if isnan(table.loc[i].R):
            ray[-1].u = ray[-2].u
        else:
            ray[-1].u = (ray[-2].n * 
               ray[-2].u - ray[-1].y*(ray[-1].n-ray[-2].n)
               /(table.loc[i].R) * (-1 if inverted else 1))/(ray[-1].n)        
   
    return ray

# Berechne Position und Lage der Eintrittspupille
def calcEP(table):
    # Eintrittspupille - Position
    startI = table.loc[table['type']=='S'].index[0] # Index des ersten Stops
    # Randbedingungen zur Bestimmung der Position der Eintrittspupille:
    startY = 0 
    startU = 0.1
    rayDEP = calcYNU(table, [startI, startY, startU], inverted=True)
    dEP = -rayDEP[-2].y/rayDEP[-2].u # d_AP = -y/u
    
    # Eintrittspupille - Höhe
    startI = table.loc[table['type']=='S'].index[0] # Index des ersten Stops
    # Randbedingungen zur Bestimmung der Höhe der Eintrittspupille:
    startY = table.loc[table['type']=='S', 'z'].iloc[0] # Höhe des Stops
    startU = 0
    rayHEP = calcYNU(table, [startI, startY, startU], inverted=True)
    hEP = rayHEP[-2].y + rayHEP[-2].u * dEP # h_EP = y + u*d_EP
    return [dEP, hEP]

# Berechne Position und Lage der Austrittspupille
def calcAP(table):
    # Austrittspupille - Position
    startI = table.loc[table['type']=='S'].index[0] # Index des ersten Stops
    # Randbedingungen zur Bestimmung der Position der Austrittspupille:
    startY = 0 
    startU = 0.1
    rayDAP = calcYNU(table, [startI, startY, startU])
    dAP = -rayDAP[-1].y/rayDAP[-1].u # d_AP = -y/u
    
    # Austrittspupille - Höhe
    startI = table.loc[table['type']=='S'].index[0] # Index des ersten Stops
    # Randbedingungen zur Bestimmung der Höhe der Austrittspupille:
    startY = table.loc[table['type']=='S', 'z'].iloc[0] # Höhe des Stops
    startU = 0
    rayHAP = calcYNU(table, [startI, startY, startU])
    hAP = rayHAP[-1].y + rayHAP[-1].u * dAP # h_EP = y + u*d_EP
    return [dAP, hAP]


# Berechne back focal length (rückwertige Fokallänge)
def calcBFL(table):
    # Randbedingungen zur Bestimmung der bfl:
    startI = 0 
    startY = 1 
    startU = 0
    # Strahl berechnen
    ray = calcYNU(table, [startI, startY, startU])
    # bfl = -y/u
    bfl = -ray[-1].y/ray[-1].u 
    return bfl

# Berechne front focal length (vordere Fokallänge)
def calcFFL(table):
    # Randbedingungen zur Bestimmung der ffl:
    startI = len(table)-1
    startY = 1 
    startU = 0
    # Strahl berechnen
    ray = calcYNU(table, [startI, startY, startU], inverted=True)
    # ffl = -y/u
    ffl = ray[-2].y/ray[-2].u 
    return ffl

# Berechne effective focal length (effektive Fokallänge)
def calcEFL(table):
    # Randbedingungen zur Bestimmung der ffl:
    startI = len(table)-1
    startY = 1 
    startU = 0
    # Strahl berechnen
    ray = calcYNU(table, [startI, startY, startU], inverted=True)
    # ffl = -y/u
    efl = -ray[0].y/ray[-2].u 
    return efl

# Berechne (paraxial) korrekte Bildposition
def calcDImage(table):
    ray = calcYNU(table, [0, 0, 0.01])
    dImage = -ray[-1].y/ray[-1].u
    return dImage

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
    
    # Bild einzeichnen
    for index, obj in table.iterrows():
       if obj.type == 'I' :
           ax.arrow(table[:index+1].x.sum(), 0, 0, obj.z-obj.z/10, head_width=4, head_length=obj.z/10, fc='k', ec='k')

           
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
    plt.savefig("temp.png") 