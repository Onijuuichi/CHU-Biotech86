# -*- coding: utf-8 -*-
"""
Créé le 13/12/2022; MAJ le 14/12/2022
@Author : FERNANDES Manon, PERARD Nolwenn, ROUILLARD Solenne, SCHNEIDEWIND Shanna
"""

#---------------------------Modules à importer---------------------------#

import sys
sys.path.append("..")

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.scrolledtext as st

import sys
import json
import re



#---------------------------Développement---------------------------#

class Interface():
    
    is_on=True

    def __init__(self): 


        #Création de la fenêtre
        self.fenetre = Tk()

        #Donne un titre à la fenêtre
        self.fenetre.title("CHU-Biotech86")

        #Donne la taille de la fenêtre
        self.fenetre.geometry("500x400")

        #Type des fichiers utilisés
        self.Type = [("Fichier CSV", ".csv")]
        self.png = [("Fichier PNG", ".png")]

        # Define Our Images
        self.on = PhotoImage(file = "on.png")
        self.off = PhotoImage(file = "off.png")

        #Création de la barre de menu
        self.menubar = Menu(self.fenetre)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="Aide", command=self.aide)

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="Réinitialiser la liste", command=self.reset)

        self.fenetre.config(menu=self.menubar)

        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitter)

        self.ok = False
        self.oldcanvas = False
     
        self.on_button = Button(self.fenetre, image = self.on, bd = 0, command = self.switch)
        self.on_button.grid(row=6, column=1, padx=15, sticky=W)
    
    #Affichage de la fenêtre
    def run(self):
        self.contenuFenetre()
        self.fenetre.mainloop()  
        
    #Création de la fenêtre "Aide"
    def aide(self):
      self.fenetreAide = Tk()
      self.fenetreAide.title("Aide")

      #Texte de la fenêtre "Aide"
      self.champ_label = Label(self.fenetreAide, text="Bienvenue dans la fenêtre 'Aide' !")
      self.champ_label.grid(row=1, column=0)
      self.champ_label = Label(self.fenetreAide, text="")
      self.champ_label.grid(row=2, column=0, sticky=W)

    #Quitter l'application
    def quitter(self):
        self.quitte = messagebox.askquestion ('Quitter', 'Voulez-vous vraiment quitter ?' , icon = 'error')
        if self.quitte == 'yes':
            self.fenetre.destroy()

    #Reset la liste
    def reset(self):
        if self.oldcanvas:
            self.canvas.get_tk_widget().destroy()

    #Création du formulaire
    def contenuFenetre(self):
 
        self.titre = StringVar()

        #Create my label
        self.labelPhen = Label(self.fenetre, text = "Entrer un charactère phenotypique", font=('arial',9,'bold'))
        self.labelPhen.grid(row = 0, column = 0, padx=20, pady=15, sticky=W)
        self.entryPhen = Entry(self.fenetre, bg='white', textvariable=self.titre)
        self.entryPhen.grid(row = 1, column = 0, padx=15, sticky=W)

        self.textArea= st.ScrolledText(self.fenetre).grid(row=1, column=2, padx=15, sticky=W)

        self.buttonEnter = Button(self.fenetre, text = "Entrer")
        self.buttonEnter.grid(row = 3, column = 0, padx=15, pady=15, sticky=W)

        self.buttonExport = Button(self.fenetre, text ="Exporter")
        self.buttonExport.grid(row = 3, column = 1, padx=15, sticky=W)
        

    def switch(self):
        
        #if my button was on
        if self.is_on:
            self.on_button.config(image = self.off)
            self.labelPhen.config(text = "Enter a phenotypic characteristic")
            self.labelPhen.grid(row = 0, column = 0, padx=20, pady=15, sticky=W)

            self.buttonEnter.config(text = "Enter")
            self.buttonEnter.grid(row = 3, column = 0, padx=15, pady=15, sticky=W)

            self.buttonExport.config(text ="Export")
            self.buttonExport.grid(row = 3, column = 1, padx=15, sticky=W)

            self.is_on = False

        
        #if my button was off
        else:
            self.on_button.config(image = self.on)
            self.labelPhen.config(text = "Entrer un caractère phénotypique")
            self.labelPhen.grid(row = 0, column = 0, padx=20, pady=15, sticky=W)

            self.buttonEnter.config(text = "Entrer")
            self.buttonEnter.grid(row = 3, column = 0, padx=15, pady=15, sticky=W)

            self.buttonExport.config(text ="Exporter")
            self.buttonExport.grid(row = 3, column = 1, padx=15, sticky=W)
            
            self.is_on = True        
        
#---------------------------Run---------------------------#

    
if __name__ == '__main__' :
    app = Interface()
    app.run()
