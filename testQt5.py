import os
import sys
from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QCompleter, QWidget, QFileDialog
from PyQt5.uic import loadUi
from numpy import loadtxt
import codecs

class fenetre(QWidget):
    def __init__(self):
        #Création et paramétrage de la fenêtre :
        super(fenetre, self).__init__()
        loadUi('fenetre.ui',self)
        self.setWindowTitle('Phen2HPO')
        self.setFixedSize(self.size()); #pour ne pas pouvoir redimensionner la fenetre

        #================= POUR L'AUTO-COMPLETION =====================================================================#
        #Création de la liste des mots qui seront suggérés à l'utilisateur :
        fichier_HPO = codecs.open("HPO_FR.txt", encoding='utf-8') #pour définir le fichier + accepter les accents avec 'utf-8'
        list_autocompletion = loadtxt(fichier_HPO, dtype=str, comments="#", delimiter="\n", unpack=False)

        #Création du 'completer' associé à la liste des mots/suggestions:
        completer = QCompleter(list_autocompletion)
        #Initialisation du mode de filtrage pour les suggestions
        #Ici 'MatchContains' permets de suggérer toutes les lignes contenant la saisie, peut importe sa position dans la ligne
        #Par exemple, si on saisie "sco" en FR, cela va nous retourner "Scotome", "Scoliose", "Faible score APGAR", ...
        completer.setFilterMode(Qt.MatchContains)
        #Et faire en sorte qu'il n'y ait pas de soucis avec les majuscules/minuscules
        #Par exemple, si on saisie "sco" en FR, cela peut quand même retourner le terme "Scoliose" (qui commence par une majuscule)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        #Ajout du completer à notre input pour la saisie "lineEdit"
        self.lineEdit.setCompleter(completer)

    @pyqtSlot()
    def on_addButton_clicked(self):
        #Ajoute l'élément dans la liste (visible sur l'interface) :
        if self.lineEdit.text()!="":
            QListWidgetItem(self.lineEdit.text(), self.listWidget)

    @pyqtSlot()
    def on_deleteButton_clicked(self):
        listItems = self.listWidget.selectedItems() #Récupération des éléments sélectionnés

        #Suppression des éléments de la liste qui sont sélectionnés:
        if not listItems: return
        for item in listItems:
            self.listWidget.takeItem(self.listWidget.row(item)) #suppression des items de la liste

    @pyqtSlot()
    def on_exportButton_clicked(self):
        #Création du fichier :
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'),"Text files (*.txt)")
        if file_name != "":
            with open(file_name, 'w') as f:
                #Pour chaque élément de la liste:
                for index in range(self.listWidget.count()):
                    text = self.listWidget.item(index).text() #récupérer le texte
                    f.write(text+"\n") #et l'ajouter dans le fichier


app=QApplication(sys.argv)
widget=fenetre()
widget.show()
sys.exit(app.exec_())