import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfile, askopenfilename 
import os

#import matplotlib
#matplotlib.use('TkAgg')
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure

text_hilfe = """Die einzulesenden Dateien sollten bitte wie folgt aussehen:
                  \nO\tobject.x\t\tobject.z\t\tobject.n 
                  \nL\tsurface.x\t\tsurface.r\t\tsurface.n\t\tsurface.d 
                  \nM\tmirror.x\t\tmirror.r\t\tmirror.n\t\tmirror.d 
                  \nS\tstop.x\t\tstop.d 
                  \n\n\nDie einzelnen Attribute sind jeweils mit einem Tabulator getrennt.
                  """
                  
                  
#Button f. Auswahl der Datei
#open_button = Button(window, text ='Open', command = lambda:open_file()) 
#open_button.pack(side = TOP, pady = 10) 

#Button f. Beenden des Fensters
#exit_button = Button(window, text ='Exit', command = window.destroy) 
#exit_button.pack(side = BOTTOM, pady = 10) 


#Aufruf der Datei
def open_file(): 
    file = askopenfilename(initialdir = os.getcwd(), filetypes =[('Text Files', '*.txt'), ("all files","*.*")]) 
    if file is not None: 
        print('Ausgewähltes System:', file) 
    #file.close()
    return file

def open_window():
    #Einstellungen d. Hauptfensters
    window = tk.Tk()
    window.title("Raytracing")
    window.geometry('600x600')
    #Menübutton mit Reiter
    menu_button = Menubutton(window, text = 'Menü', relief = RAISED, justify = "left")
    menu_button.menu = Menu (menu_button, tearoff = 0)
    menu_button["menu"] =  menu_button.menu
    menu_button.menu.add_checkbutton (label="Datei öffnen", command = lambda:open_file())
    menu_button.menu.add_checkbutton (label="Hilfe", command = lambda:open_syntax())
    menu_button.menu.add_separator()
    menu_button.menu.add_checkbutton ( label="Beenden", command = window.destroy)
    menu_button.pack(anchor='nw')
    #Loop f. Benutzereingabe
    window.mainloop() 

#Aufruf d. Syntax zur Hilfe
def open_syntax(): 
    syntax_window = tk.Tk()
    syntax_window.geometry('600x500')
    syntax_window.title("Syntax")
    syntax_text = tk.Text(syntax_window)
    syntax_text.pack()
    syntax_text.insert(tk.END, text_hilfe)
    syntax_window.pack()
    syntax_window.mainloop()
    
