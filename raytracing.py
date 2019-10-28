#Aufrufen der Datei im Kommandofenster: python raytracing.py test.txt

# Import
from raytracing_functions import loadOptSystem, ynu, invertTable, calcYNU, plotOptSystem
import sys


# Lade optisches System
table = loadOptSystem(sys.argv[1])

#table = invertTable(table)
        
# Surfaces berechnen
strahl = calcYNU(table)

# Darstellung des Strahlenganges
plotOptSystem(strahl, table)
