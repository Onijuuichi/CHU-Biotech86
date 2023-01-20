import os
import sys
from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QCompleter, QWidget, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
from numpy import loadtxt
import codecs

class fenetre(QMainWindow):
    def __init__(self):
        #Création et paramétrage de la fenêtre :
        super(fenetre, self).__init__()
        loadUi('fenetre_avec_menu.ui',self)
        self.setWindowTitle('Phen2HPO')
        self.setMinimumSize(800, 500) #pour la taille minimum de la fenetre / @param : self.setMinimumSize(width, height)
        #self.setFixedSize(self.size()); #pour ne pas pouvoir redimensionner la fenetre

        #Setting de la langue de l'application :
        self.on_francaisButton_clicked()

    @pyqtSlot()
    def on_addButton_clicked(self):
        #Ajoute l'élément dans la liste (visible sur l'interface) :
        if self.lineEdit.text()!="":
            
            deja_present=False #initialisation variable

            #Regarder dans tous les éléments de la liste :
            for index in range(self.listWidget.count()):
                    #Pour vérifier si l'élément a déjà été ajouté
                    if self.lineEdit.text()==self.listWidget.item(index).text():
                        deja_present=True #Alors on mets à True

            #Si l'élement n'est pas déjà présent, alors ajout :
            if deja_present==False:
                QListWidgetItem(self.lineEdit.text(), self.listWidget)

        self.lineEdit.setText("")

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

    @pyqtSlot()
    def on_englishButton_clicked(self):
        #Traduction de l'ensemble des éléments :
        self.label_langue.setText('Please select a language :')
        self.label_aide.setText('Help text')
        self.label_1.setText('Please select a phenotype')
        self.label_2.setText('Patients phenotype list')

        self.addButton.setText('✓ Add')
        self.deleteButton.setText('✗ Delete the selected element')
        self.exportButton.setText('Export ❯❯')

        self.tabWidget.setTabText(0,'Phenotype entry')
        self.tabWidget.setTabText(1,'Help')
        self.tabWidget.setTabText(2,'Language')

        self.set_autocompleter('EN')
        self.reset_list_language('EN')

    @pyqtSlot()
    def on_francaisButton_clicked(self):
        #Traduction de l'ensemble des éléments :
        self.label_langue.setText('Veuillez saisir la langue pour l\'application :')
        self.label_aide.setText('Texte pour l\'aide')
        self.label_1.setText('Veuillez-saisir un phénotype :')
        self.label_2.setText('Liste des phénotypes du patient')

        self.addButton.setText('✓ Ajouter')
        self.deleteButton.setText('✗ Supprimer les élément(s) sélectionné(s)')
        self.exportButton.setText('Enregistrer ❯❯')

        self.tabWidget.setTabText(0,'Saisie phenotype')
        self.tabWidget.setTabText(1,'Aide')
        self.tabWidget.setTabText(2,'Langue')

        self.set_autocompleter('FR')
        self.reset_list_language('FR')

    @pyqtSlot()
    def set_autocompleter(self, string):
        #Verification quel langue choisie:
        if string=="FR":
            nom_fichier="HPO_FR.txt" #Langue française choisie, utiliser le fichier avec les termes en français
            #print('Fichier en FR utiliser pour le completer') #verification
        else:
            nom_fichier="HPO_EN.txt" #Langue anglaise choisie, utiliser le fichier avec les termes en anglais
            #print('Fichier en EN utiliser pour le completer') #verification

        #================= POUR L'AUTO-COMPLETION =====================================================================#
        #Création de la liste des mots qui seront suggérés à l'utilisateur :
        fichier_HPO = codecs.open(nom_fichier, encoding='utf-8') #pour définir le fichier + accepter les accents avec 'utf-8'
        list_autocompletion, trash = loadtxt(fichier_HPO, dtype=str, comments="$", delimiter="#", unpack=True)
        
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
    def reset_list_language(self, string):
        #Verification de la langue choisie, pour mettre les bons termes:
        if string=="FR":
            fichier_langue_avant="HPO_EN.txt" #avant de cliquer sur le bouton, c'était en anglais
            fichier_langue_apres="HPO_FR.txt" #l'utilisateur veut que ça soit en français mtn
            #fichierprint('FR')

        else:
            fichier_langue_avant="HPO_FR.txt" #avant de cliquer sur le bouton, c'était en français
            fichier_langue_apres="HPO_EN.txt" #l'utilisateur veut que ça soit en anglais mtn
            #fichierprint('EN')
        
        #Création de la liste des termes phen/HPO :
        fichier_HPO = codecs.open(fichier_langue_apres, encoding='utf-8') #pour définir le fichier + accepter les accents avec 'utf-8'
        liste_termes, trash = loadtxt(fichier_HPO, dtype=str, comments="$", delimiter="#", unpack=True)
        
        #Pour chaque élément de la liste:
        for index in range(self.listWidget.count()):
            ligne = self.listWidget.item(index).text().split() #récupérer le texte et de manière coupé
            #par ex, ça va donner : ['Anomalie', 'de', 'la', 'taille', 'corporelle', 'HP:0000002']
            
            # ligne[-1] : -1 pour avoir le dernier élément, se sera toujours le terme HPO
            
            matching = [s for s in liste_termes if ligne[-1] in s]
            self.listWidget.item(index).setText(str(matching[0]))
            #print(matching) #verification // celon le terme, parfois il y en a plusieurs, donc on mets l'index 1


app=QApplication(sys.argv)
widget=fenetre()
widget.show()
sys.exit(app.exec_())