import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QListWidgetItem, QCompleter, QLineEdit, QWidget
from PyQt5.uic import loadUi

class fenetre(QWidget):
    def __init__(self):
        super(fenetre, self).__init__()
        loadUi('fenetre.ui',self)
        self.setWindowTitle('Notre Interface')

        #Pour l'auto-complétion :
        list_autocompletion = ["coucou", "banana", "anana"]
        completer = QCompleter(list_autocompletion)

        self.lineedit = QLineEdit()
        self.lineedit.setCompleter(completer)

        for txt in list_pheno:
            QListWidgetItem(txt, self.listWidget)

#Liste dynamique :
#https://stackoverflow.com/questions/35074199/filling-a-qlistwidget-with-elements-from-a-dynamic-list

list_pheno = ["coucou","banana","anana"]

app=QApplication(sys.argv)
widget=fenetre()
widget.show()
sys.exit(app.exec_())