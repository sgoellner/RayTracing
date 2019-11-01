#Aufrufen der Datei im Kommandofenster: python raytracing.py test.txt

# Import
from raytracing_functions import loadOptSystem, ynu, invertTable, calcYNU, plotOptSystem
import sys


# Lade optisches System
table = loadOptSystem(sys.argv[1])

# Surfaces berechnen
strahl = calcYNU(table, [0, 0, 0.1])
strahl2 = calcYNU(table, [0, 10, 0])

# Darstellung des Strahlenganges
plotOptSystem(table, [strahl,strahl2])
