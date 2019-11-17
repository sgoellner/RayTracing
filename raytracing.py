#Aufrufen der Datei im Kommandofenster: python raytracing.py test.txt

# Import
import raytracing_functions as rt
import sys


# Lade optisches System
table = rt.loadOptSystem(sys.argv[1])

# Eintrittspupille berechnen
ep = rt.calcEP(table)
print("dEP = {} mm".format(round(ep[0],2)))
print("hEP = {} mm".format(round(ep[1],2)))

# Austrittspupille berechnen 
ap = rt.calcAP(table)
print("dAP = {} mm".format(round(ap[0],2)))
print("hAP = {} mm".format(round(ap[1],2)))

# bfl berechnen 
bfl = rt.calcBFL(table)
print("bfl = {} mm".format(round(bfl,2)))

# ffl berechnen 
ffl = rt.calcFFL(table)
print("ffl = {} mm".format(round(ffl,2)))
 
# efl berechnen 
efl = rt.calcEFL(table)
print("efl = {} mm".format(round(efl,2)))

# Bildposition berechnen und in table schreiben
dImage = rt.calcDImage(table)
table.loc[len(table)-1, 'x'] += dImage
print("dI = {} mm".format(round(table.loc[len(table)-1, 'x'], 2)))

# Surfaces berechnen
uMR = ep[1]/(table.loc[1].x-ep[0])
uCR = -table.loc[0].z/(table.loc[1].x-ep[0])
marginalRay = rt.calcYNU(table, [0, 0, uMR])
chiefRay = rt.calcYNU(table, [0, table.loc[0,'z'], uCR]) 

# Bildhöhe in table schreiben
table.loc[len(table)-1, 'z'] = chiefRay[-1].y

# Abbildungsmaßstab berechnen
beta = rt.calcMagnification(table)
print("beta = {}".format(round(beta, 2)))

# Hauptebenen berechnen
H1, H2 = rt.calcPrinciplePlanes(ffl, bfl, efl)
print("H1 = {} mm".format(round(H1, 2)))
print("H2 = {} mm".format(round(H2, 2)))

# f-Zahl berechnen
fNumber = rt.calcFNumber(efl, ep[1])
print("beta = {}".format(round(fNumber, 2)))

# Berechne objektseitige numerische Apertur
NAo = rt.calcNAO(chiefRay)
print("NA_o = {:.3f}".format(round(NAo, 3)))

# Berechne bildseitige numerische Apertur
NAi = rt.calcNAI(chiefRay)
print("NA_i = {:.3f}".format(round(NAi, 3)))


# Darstellung des Strahlenganges
rt.plotOptSystem(table, [marginalRay, chiefRay])
