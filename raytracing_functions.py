import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from math import sin, pi, inf, isnan
import pandas as pd
import numpy
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
def loadOptSystem(fileName):
    # Lade Datei in table
    try:
        table = pd.read_csv(fileName, sep = '\t')
    except IndexError:
        print("Error! Datei mit Linsensystem nicht als Parameter angegeben!")
        sys.exit(1)
    except FileNotFoundError:
        print("Error! Datei \"{}\" konnte nicht gefunden werden"
              .format(sys.argv[1]))
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
        
    # Datentypen prüfen
    # table.type: str
    # table.x, table.z, table.n, table.R: int,float, numpy.int64, numpy.float64
    for i in range(len(table)):
        if not isinstance(table.loc[i, 'type'], str):
            print(("Fehler! Falscher Datentyp! "
                  "Kein String in Spalte 'type', Zeile {}!").format(i+2))
            sys.exit(1)
        if not isinstance(table.loc[i, 'x'], 
                          (int, float, numpy.int64, numpy.float64)):
            print(("Fehler! Falscher Datentyp! "
                  "Keine Zahl in Spalte 'x', Zeile {}!").format(i+2))
            sys.exit(1)
        if not isinstance(table.loc[i, 'z'], 
                          (int, float, numpy.int64, numpy.float64)):
            print(("Fehler! Falscher Datentyp! "
                  "Keine Zahle in Spalte 'z', Zeile {}!").format(i+2))
            sys.exit(1)
        if not isinstance(table.loc[i, 'n'], 
                          (int, float, numpy.int64, numpy.float64)):
            print(("Fehler! Falscher Datentyp! "
                  "Keine Zahl in Spalte 'n', Zeile {}!").format(i+2))
            sys.exit(1)
        if not isinstance(table.loc[i, 'R'], 
                          (int, float, numpy.int64, numpy.float64)):
            print(("Fehler! Falscher Datentyp! "
                  "Keine Zahl in Spalte 'R', Zeile {}!").format(i+2))
            sys.exit(1)
        
    # Typen prüfen    
    for i in range(len(table)):
        # Alle Typen in Uppercase umwandeln
        table.loc[i, 'type'] = table.loc[i, 'type'].upper()
        # Typen prüfen: Nur O, L, S, I
        if table.loc[i, 'type'] not in ['O', 'L', 'S', 'I']:
            print("Fehler! Unbekannter Typ {} in Zeile {}!".
                  format(table.loc[i, 'type'], i+2))
            sys.exit(1)
            
    # Erste Zeile = Objekt?
    if table.type[0] != 'O':
        print('Fehler! Erste Zeile muss das Objekt (O) darstellen!')
        sys.exit(1)
        
    # Genau ein Objekt vorhanden?
    try:
        if table.type.value_counts()['O'] != 1:
            print('Fehler! Es ist nicht ein Objekt, sondern {} vorhanden!'
                  .format(table.type.value_counts()['O']))
            sys.exit(1)
    except KeyError: # Kein 'O' gefunden?
        print("Fehler! Kein Objekt angegeben!")
        sys.exit(1)
        
    # Genau ein Stop vorhanden?
    try:
        if table.type.value_counts()['S'] != 1:
            print('Fehler! Es ist nicht ein Stop, sondern {} vorhanden!'
                  .format(table.type.value_counts()['S']))
            sys.exit(1)
    except KeyError:
        print("Fehler! Kein Stop angegeben!")
        sys.exit(1)
        
    # Radius prüfen
    for i in range(len(table)):
        if table.R[i] == 0:
            print('Fehler! Radius darf nicht 0 sein')
            sys.exit(1) 
        
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

# Berechne Abbildungsmaßstab
def calcMagnification(table):
    return table.loc[len(table)-1, 'z']/table.loc[0, 'z']

# Berechne Hauptebenen
def calcPrinciplePlanes(ffl, bfl, efl):
    return ffl + efl, bfl - efl

# Berechne f-Zahl
def calcFNumber(efl, hEP):
    return efl/(2*hEP)

# Berechne objektseitige numerische Apertur
def calcNAO(chiefRay):
    return abs(chiefRay[0].n * chiefRay[0].u)

# Berechne bildseitige numerische Apertur
def calcNAI(chiefRay):
    return abs(chiefRay[-1].n * chiefRay[-1].u)

# Berechne sphärische Seidel-Aberrationen (S_1)
def calcSeidel1(table, marginalRay):
    aberrations = []
    for i in range(len(table)):
        
        aberrations.append(
                -marginalRay[i-1].n**2 * marginalRay[i].y * (
                marginalRay[i].y/table.loc[i, 'R'] + marginalRay[i-1].u)**2 * (
                marginalRay[i].u/marginalRay[i].n -
                marginalRay[i-1].u/marginalRay[i-1].n)
                )
                
        #print("-{}**2 * {} * ({}/{} + {}) * ({}/{} - {}/{})".format(marginalRay[i-1].n, marginalRay[i].y, marginalRay[i].y, table.loc[i, 'R'], marginalRay[i-1].u, marginalRay[i].u, marginalRay[i].n, marginalRay[i-1].u, marginalRay[i-1].n))
        #print("=", aberrations[-1])
    return aberrations


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
            l = mlines.Line2D([ray[i-2].x,ray[i-1].x], 
                              [ray[i-2].y, ray[i-1].y])
            ax.add_line(l)     
    
    # Objekt einzeichnen
    for index, obj in table.iterrows():
       if obj.type == 'O' :
           ax.arrow(obj.x, 0, 0, obj.z-obj.z/10,
                    head_width=4, head_length=obj.z/10, fc='k', ec='k')
    
    # Bild einzeichnen
    for index, obj in table.iterrows():
       if obj.type == 'I' :
           ax.arrow(table[:index+1].x.sum(), 0, 0, obj.z-obj.z/10, 
                    head_width=4, head_length=obj.z/10, fc='k', ec='k')

           
    # Linsenflächen einzeichnen
    for index, surface in table.iterrows():
        if surface.type == 'L' :
            if surface.R == inf:
                surface.R = 1e10
            # Winkel des Bogens aus Höhe der Linse berechnen
            theta = sin(surface.z/surface.R)*180/pi
            # Winkel negieren, wenn Linse konkav
            if surface.R < 0:
                theta = -theta
            arc = Arc((table[:index+1].x.sum()+surface.R, 0), 
                      2*surface.R, 2*surface.R, 0, -theta-180, theta-180, 
                      edgecolor ='b', facecolor ='none')
            patches.append(arc)
            ax.add_artist(arc)
    
    
    # Stop Einzeichnen
    for index, stop in table.iterrows():
      if stop.type == 'S' :
          ax.vlines(table[:index+1].x.sum(), stop.z, table[:index+1].z.sum(), 
                    colors='r', linestyles='solid', label='') 
          ax.vlines(table[:index+1].x.sum(), -stop.z, -table[:index+1].z.sum(),
                    colors='r', linestyles='solid', label='') 
       
    # Achsenbegrenzungen berechnen und setzen
    # x: von min bis max mit jeweils 1/50 der Länge des opt. Systems als Rand
    # y: von min bis max mit jeweils 1/10 der maximalen Höhe als Rand
    xlim=[table.x[0]-table[:].x.sum()/50, table[:].x.sum()+table[:].x.sum()/50]
    ylim=[-1.1*table[:].z.max(), 1.1*table[:].z.max()]
    ax.set(xlim=xlim, ylim=ylim)
    #ax.set(xlim=[-20, 40], ylim=ylim)
    
    # Optische Achse einzeichnen
    plt.plot(xlim, [0,0], color='grey', linewidth=1, linestyle='dashdot')

    # Achsenbeschriftungen setzen und plot erzeugen
    plt.xlabel('opt. Achse in mm')
    plt.ylabel('z in mm')
    plt.show




