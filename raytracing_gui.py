import tkinter as tk
import raytracing_functions as rt
from tkinter import *
from tkinter.filedialog import askopenfilename 
from PIL import ImageTk, Image
import os

text_hilfe = """Die einzulesenden Dateien sollten bitte wie folgt aussehen:
                  \nO\tobject.x\t\tobject.z\t\tobject.n 
                  \nL\tsurface.x\t\tsurface.r\t\tsurface.n\t\tsurface.d 
                  \nM\tmirror.x\t\tmirror.r\t\tmirror.n\t\tmirror.d 
                  \nS\tstop.x\t\tstop.d 
                  \n\n\nDie einzelnen Attribute sind jeweils mit einem Tabulator getrennt.
                  """

#Einstellungen d. Hauptfensters
def open_window():
    global window
    window = tk.Tk()
    window.title("Raytracing")
    window.geometry('600x600')
    #Menübutton mit Reiter
    menu_button = Menubutton(window, text = 'Menü', relief = RAISED, justify = "left")
    menu_button.menu = Menu (menu_button, tearoff = 0)
    menu_button["menu"] =  menu_button.menu
    menu_button.menu.add_checkbutton(label="Datei öffnen", command = lambda:loadAll())
    menu_button.menu.add_checkbutton(label="Hilfe", command = lambda:open_help())
    menu_button.menu.add_separator()
    menu_button.menu.add_checkbutton( label="Beenden", command = window.destroy)
    menu_button.pack(anchor='nw')
    window.grid()
    #Loop f. Benutzereingabe
    window.mainloop()

def loadAll():
    window.update()
    global ep, ap, bfl, ffl, efl, dImage
    table = rt.loadOptSystem()
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
    # Darstellung des Strahlenganges
    rt.plotOptSystem(table, [marginalRay, chiefRay])
    #Anzeige der Ergebnisse von EP,AP, (...) im Fenster
    window_results()
    #Anzeige d. des Strahlenverlaufes im Fenster
    window_plot()
    

#Aufruf d. Syntax zur Hilfe
def open_help(): 
    help_window = tk.Tk()
    help_window.geometry('600x500')
    help_window.title("Help")
    help_text = tk.Text(help_window)
    help_text.pack()
    help_text.insert(tk.END, text_hilfe)
    help_window.pack()
    help_window.mainloop()
    pass

#Anzeige der Berechneten Größen im Fenster
def window_results():
    results_text = tk.Text(window)
    results_text.pack()
    results_text.insert(tk.END,"dep \t %s mm" %round(ep[0],2))
    results_text.insert(tk.END,"\nhep \t %s mm" %round(ep[1],2))
    results_text.insert(tk.END,"\ndap \t %s mm" %round(ap[0],2))
    results_text.insert(tk.END,"\nhep \t %s mm" %round(ep[1],2))
    results_text.insert(tk.END,"\nbfl \t %s mm" %round(bfl,2))
    results_text.insert(tk.END,"\nffl \t %s mm" %round(ffl,2))
    results_text.insert(tk.END,"\nefl \t %s mm" %round(efl,2))
    results_text.insert(tk.END,"\ndI \t %s mm" %round(dImage,2))
    window.update()
    pass
        
#Anzeige des Plots im Fenster
def window_plot():
    img_path = os.path.join(os.path.dirname(__file__),"temp.png")
    img = ImageTk.PhotoImage(file = img_path)
    panel = Label(window, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    window.update()
    window.mainloop()
    pass