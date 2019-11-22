#Aufrufen der Datei im Kommandofenster: python raytracing.py test.txt

# Import
import raytracing_functions as rt
import sys


# Lade optisches System
table = rt.loadOptSystem(sys.argv[1])

# Eintrittspupille berechnen
ep = rt.calcEP(table)
print("dEP = {} mm\t hEP = {} mm".format(round(ep[0],2), round(ep[1],2)))

# Austrittspupille berechnen 
ap = rt.calcAP(table)
print("dAP = {} mm\t hAP = {} mm".format(round(ap[0],2), round(ap[1],2)))

# bfl, ffl, efl berechnen 
bfl = rt.calcBFL(table) 
ffl = rt.calcFFL(table) 
efl = rt.calcEFL(table)
print("efl = {} mm\t ffl = {} mm\t bfl = {} mm".
      format(round(efl,2), round(ffl,2), round(bfl,2)))

# Bildposition berechnen und in table schreiben
dImage = rt.calcDImage(table)
table.loc[len(table)-1, 'x'] += dImage
print("dI = {} mm".format(round(table.loc[len(table)-1, 'x'], 2)))
if dImage < 0: print("Bild ist virtuell.")

# Haupt- und Randstrahl berechnen
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
print("H1 = {} mm\t H2 = {} mm".format(round(H1, 2), round(H2, 2)))

# f-Zahl berechnen
fNumber = rt.calcFNumber(efl, ep[1])
print("f-Zahl = {}".format(round(fNumber, 2)))

# Berechne objektseitige und bildseitige numerische Apertur
NAo = rt.calcNAO(chiefRay)
NAi = rt.calcNAI(chiefRay)
print("NA_i = {:.3f}\t NA_o = {:.3f}".format(round(NAi, 3), round(NAo, 3)))

S1 = rt.calcSeidel1(table, marginalRay)
print("Sphärische Seidelaberrationen:")
for i in range(len(S1)):
    print("#{}\t{: .4f} mm".format(i, S1[i]))
print("S1_ges\t{: .4f} mm".format(sum(S1)))

# Darstellung des Strahlenganges
rt.plotOptSystem(table, [marginalRay, chiefRay])
