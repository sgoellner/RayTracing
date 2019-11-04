#Aufrufen der Datei im Kommandofenster: python raytracing.py test.txt

# Import
import raytracing_functions as rt
import sys


# Lade optisches System
table = rt.loadOptSystem(sys.argv[1])

# Surfaces berechnen
ray = rt.calcYNU(table, [0, 0, 0.03])
ray2 = rt.calcYNU(table, [0, table.loc(0,'z'), 0])

# Darstellung des Strahlenganges
rt.plotOptSystem(table, [ray, ray2])
