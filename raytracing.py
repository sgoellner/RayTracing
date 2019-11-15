#Aufrufen der Datei im Kommandofenster: python raytracing.py test.txt

# Import
import raytracing_functions as rt
import sys


# Lade optisches System
table = rt.loadOptSystem(sys.argv[1])

# Surfaces berechnen
ray = rt.calcYNU(table, [0, 0, 0.07])
ray2 = rt.calcYNU(table, [0, table.loc[0,'z'], 0])

# Eintrittspupille berechnen
ep = rt.calcEP(table)
print("dEP = {} mm".format(round(ep[0],2)))
print("hEP = {} mm".format(round(ep[1],2)))

# Austrittspupille berechnen 
ap = rt.calcAP(table)
print("dAP = {} mm".format(round(ap[0],2)))
print("hAP = {} mm".format(round(ap[1],2)))
 

# Darstellung des Strahlenganges
rt.plotOptSystem(table, [ray, ray2])
