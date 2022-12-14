# -*- coding: utf-8 -*-
"""
Crée le 13/12/2022
@Author : FERNANDES Manon, PERARD Nolwenn, ROUILLARD Solenne, SCHNEIDEWIND Shana
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


    def reset(self):
        if self.oldcanvas:
            self.canvas.get_tk_widget().destroy()
    
    #Création du formulaire
    def contenuFenetre(self):

        self.titre = StringVar()
        
        self.labelPhen = Label(self.fenetre, text = "Enter a phenotypic characteristic", font=('arial',9,'bold')).grid(row = 0, column = 0, padx=20, pady=15, sticky=W)
        self.entryPhen = Entry(self.fenetre, bg='white', textvariable=self.titre).grid(row = 1, column = 0, padx=15, sticky=W)

        self.textArea= st.ScrolledText(self.fenetre).grid(row=1, column=2, padx=15, sticky=W)

        buttonEnter = Button(self.fenetre, text = "Enter").grid(row = 3, column = 0, padx=15, pady=15, sticky=W)
        buttonExport = Button(self.fenetre, text ="Export").grid(row = 3, column = 1, padx=15, sticky=W)
        
        
#---------------------------Run---------------------------#

    
if __name__ == '__main__' :
    app = Interface()
    app.run()
