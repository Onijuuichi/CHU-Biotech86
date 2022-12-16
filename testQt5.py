import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QListWidgetItem, QCompleter, QLineEdit, QWidget
from PyQt5.uic import loadUi
from numpy import loadtxt
import codecs

class fenetre(QWidget):
    def __init__(self):
        #Création et paramétrage de la fenêtre :
        super(fenetre, self).__init__()
        loadUi('fenetre.ui',self)
        self.setWindowTitle('Phen2HPO')

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

        #================= POUR AFFICHER LES PHENOTYPES CHOISIS =======================================================#
        for txt in list_phenotype:
            QListWidgetItem(txt, self.listWidget)




list_phenotype = []
#list_phenotype = ["coucou", "banana", "anana"]

app=QApplication(sys.argv)
widget=fenetre()
widget.show()
sys.exit(app.exec_())

#Liste dynamique :
#https://stackoverflow.com/questions/35074199/filling-a-qlistwidget-with-elements-from-a-dynamic-list

#Manuel pour PyQt5 :
#https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QCompleter.html#PySide2.QtWidgets.PySide2.QtWidgets.QCompleter.setFilterMode
