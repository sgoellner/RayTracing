#Functions Importieren
import raytracing_functions as rt

#Tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename 
from tkinter import ttk

#matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os

panel = []
text_hilfe = """Die einzulesenden Dateien sollten bitte wie folgt aussehen:

type\tx\t\tz\t\tn\t\tR
O\tobject.x\tobject.z\tobject.n\tnan 
L\tsurface.x\tsurface.r\tsurface.n\tsurface.d 
M\tmirror.x\tmirror.r\tmirror.n\tmirror.d 
S\tstop.x\t\tstop.d\t\tstop.n\t\tnan
I\t0\t\t0\t\t1\t\tnan

Die einzelnen Attribute sind jeweils mit einem Tabulator getrennt."""


#Einstellungen d. Hauptfensters
def openwindow():
    global window, tab_parent, tab_plot, tab_results, tab_optsystem, fig, ax
    #Mainwindow
    window = Tk()
    window.title("Raytracing")
    window.geometry('900x900')
    #Menübutton mit Reiter inkl Einstllungen
    menu_button = Menubutton(window, text = 'Menü', relief = RAISED, justify = "left")
    menu_button.menu = Menu(menu_button, tearoff = 0)
    menu_button["menu"] =  menu_button.menu
    menu_button.menu.add_checkbutton(label="Datei öffnen", command = lambda:loadAll())
    menu_button.menu.add_checkbutton(label="Hilfe", command = lambda:open_help())
    menu_button.menu.add_separator()
    menu_button.menu.add_checkbutton(label="Beenden", command = window.destroy)
    menu_button.pack(anchor='nw')
    #Einführung von Tabs
    tab_parent = ttk.Notebook(window)
    tab_plot = ttk.Frame(tab_parent)
    tab_results = ttk.Frame(tab_parent)
    tab_optsystem  = ttk.Frame(tab_parent)
    tab_parent.add(tab_plot, text="Plot")
    tab_parent.add(tab_results, text="Ergebnisse")
    tab_parent.add(tab_optsystem, text="Optisches System")
    tab_parent.pack(expand=1, fill="both")
    window.mainloop()

def loadAll():
    global fig, ax
    #fig.clear()
    #ax.clear()
    table = rt.loadOptSystem(askopenfilename(initialdir = os.getcwd(), filetypes =[('Text Files', '*.txt'), ("all files","*.*")]))
    # Eintrittspupille berechnen
    ep = rt.calcEP(table)
    # Austrittspupille berechnen 
    ap = rt.calcAP(table)
    # bfl berechnen 
    bfl = rt.calcBFL(table)
    # ffl berechnen 
    ffl = rt.calcFFL(table)
    # efl berechnen 
    efl = rt.calcEFL(table)
    # Bildposition berechnen und in table schreiben
    dImage = rt.calcDImage(table)
    table.loc[len(table)-1, 'x'] += dImage
    # Surfaces berechnen
    uMR = ep[1]/(table.loc[1].x-ep[0])
    uCR = -table.loc[0].z/(table.loc[1].x-ep[0])
    marginalRay = rt.calcYNU(table, [0, 0, uMR])
    chiefRay = rt.calcYNU(table, [0, table.loc[0,'z'], uCR]) 
    # Bildhöhe in table schreiben
    table.loc[len(table)-1, 'z'] = chiefRay[-1].y
    # Abbildungsmaßstab berechnen
    beta = rt.calcMagnification(table)
    # Hauptebenen berechnen
    H1, H2 = rt.calcPrinciplePlanes(ffl, bfl, efl)
    # f-Zahl berechnen
    fNumber = rt.calcFNumber(efl, ep[1])
    # Berechne objektseitige und bildseitige numerische Apertur
    NAo = rt.calcNAO(chiefRay)
    NAi = rt.calcNAI(chiefRay)
    # Darstellung des Strahlenganges
    fig, ax =  rt.plotOptSystem(table,
                 [marginalRay, chiefRay], rayColors=['orange', 'orange'],
                 ep=ep, ap=ap, principlePlanes=[H1, H2],
                 saveFig=False)
    canvas = FigureCanvasTkAgg(fig, master = tab_plot)
    canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = 1)
    
    
    #Anzeige der Ergebnisse von EP,AP, (...) im Fenster
    #EP
    Label(tab_results, text="dep: \t %s mm  \t nhep: \t %s mm" %(round(ep[0],2), round(ep[1],2))).grid(row=1, sticky=W)
    #AP
    Label(tab_results, text="dap: \t %s mm  \t nhap: \t %s mm" %(round(ap[0],2), round(ap[1],2))).grid(row=2, sticky=W)
    #BFL und FFL
    Label(tab_results, text="bfl: \t %s mm  \t ffl: \t %s mm" %(round(bfl,2), round(ffl,2))).grid(row=3, sticky=W)
    #EFL
    Label(tab_results, text="efl: \t %s mm" %round(efl,2)).grid(row=4, sticky=W)
    #DI
    Label(tab_results, text="nDI: \t %s mm" %round(dImage,2)).grid(row=5, sticky=W)
    # Abbildungsmaßstab
    Label(tab_results, text="beta: \t %s" %round(beta,2)).grid(row=6, sticky=W)
    #Position Hauptebenen
    Label(tab_results, text="H1: \t %s mm  \t H2: \t %s mm" %(round(H1,2), round(H2, 2))).grid(row=7, sticky=W)
    #f-Zahl
    Label(tab_results, text="f-Zahl: \t %s" %round(fNumber,2)).grid(row=8, sticky=W)
    #opjekt und bildseitige NA
    Label(tab_results, text="Numerische Apertur").grid(row=9, sticky=W)
    Label(tab_results, text="objektseitig: \t %s \t bildseitig: \t %s " %(round(NAo,2), round(NAi, 2))).grid(row=10, sticky=W)


    #Auflistung des Optischen Systems im Extra Tab
    Label(tab_optsystem, text = round(table,2)).grid(row=1, sticky=W)
    window.update()
    


#Aufruf d. Syntax zur Hilfe
def open_help(): 
    help_window = Tk()
    help_window.geometry('700x200')
    help_window.title("Help")
    hilfetext = Label(help_window, text = text_hilfe, justify=LEFT).grid(row=1, sticky=W)
    help_window.update()
    help_window.mainloop()
    