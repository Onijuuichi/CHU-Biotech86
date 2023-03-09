import os
import sys
from fuzzysearch import find_near_matches
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QCompleter, QFileDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from numpy import loadtxt
import codecs
import re
from array import *
  
class fenetre(QMainWindow):
    def __init__(self):
        #Creation and settings of the screen:
        super(fenetre, self).__init__()
        loadUi('fenetre_avec_menu.ui',self)
        self.setWindowTitle('Phen2HPO')
        self.setWindowIcon(QIcon('icon_phen2HPO.png'))
        self.setMinimumSize(800, 500) #for the minimum size of the screen / @param : self.setMinimumSize(width, height)
        #self.setFixedSize(self.size()); #to not be able to resize the screen

        #App settings:
        self.on_francaisButton_clicked() #Setting the default app language to FRENCH
        self.lineEdit.returnPressed.connect(self.addButton.click) #When "Enter" key is pressed on input, it acts as if the addButton was clicked

        self.completer.activated.connect(self.handleCompletion) #Set a custom completion handle

        self.label_warning.hide() #Hide error message

    @pyqtSlot()
    def on_addButton_clicked(self):
        #Add item in the list (visible on the interface):
        if self.lineEdit.text()!="":
            
            deja_present=False #variable initialization

            #Search in all the items of the list:
            for index in range(self.listWidget.count()):
                    #To check if the item has already been added
                    if self.lineEdit.text()==self.listWidget.item(index).text():
                        deja_present=True #So it is put on "true"

            #If the item is not already present in the saved list
            if deja_present==False:
                #Then check if the item is correct HPO term : 
                if self.lineEdit.text() in self.liste_termes:
                    #It is a correct HPO term, so we can add it to the saved list
                    QListWidgetItem(self.lineEdit.text(), self.listWidget)

                    self.label_warning.hide() #Hide error message 
                    self.lineEdit.setText("") #Clear the input

                else:
                    self.label_warning.show() #Display error message 
                    
                    #Show custom text depending on error (entry is incorrect)
                    if self.language=="FR" :
                        self.label_warning.setText("ERREUR : la saisie est incorrecte.")
                    else:
                        self.label_warning.setText("ERROR: the entry is incorrect.")
            else:
                self.label_warning.show() #Display error message 

                #Show custom text depending on error (item already in the saved list)
                if self.language=="FR" :
                    self.label_warning.setText("ERREUR : le terme choisi est déjà dans la liste.")
                else:
                    self.label_warning.setText("ERROR: the selected term is already in the list.")

    @pyqtSlot()
    def on_deleteButton_clicked(self):
        listItems = self.listWidget.selectedItems() #Fetch selected items

        #Remove items of the list that are selected:
        if not listItems: return
        for item in listItems:
            self.listWidget.takeItem(self.listWidget.row(item)) #Remove items of the list

    @pyqtSlot()
    def on_exportButton_clicked(self):
        saved_items=[]
        #Check if the lisy contains something : 
        if self.listWidget.count() != 0 :
            self.label_warning2.hide() #Hide error message 
            
            #For each element in the list viewed on the interface
            for index in range(self.listWidget.count()):

                text = self.listWidget.item(index).text() #Fetch an element in text format
                splitted_text = re.split(r'\t+', text) #Split it by the tab separating the phenotype & the HPO term
                
                #If this element is not already in the saved list (based on the HPO term - splitted_text[1])
                #Param : splitted_text[0] contains the phenotypic description, and splitted_text[1] the HPO term
                #print("splitted 0 : "+splitted_text[0]+" |||| splitted 1 : "+splitted_text[1]) #Check if it is working
                if not any([splitted_text[1] in word for word in saved_items]):
                    #Then it can be saved in the auxilary list
                    # + Editing the text line in order to have quotation marks (") before and after the phenotype
                    edited_text="\""+splitted_text[0]+"\"\t"+splitted_text[1]
                    saved_items += [edited_text]
                
            #print(saved_items) #Check if the list items are correct

            #Ask to the user if he wants to empty the lsit after export
            if self.language=="FR":
                question_export=QMessageBox.question(self, "Information", "Souhaitez-vous vider la liste après export ?", QMessageBox.Yes | QMessageBox.No)
            else:
                self.language=="EN"
                question_export=QMessageBox.question(self, "Information", "Would you like to clear the list after the export?", QMessageBox.Yes | QMessageBox.No)

            #When all elements are retrieved, we can ask where to create the CVS file :
            file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'),"Comma-separated file (*.csv)")
            
            #Then add the content of the saved list into the file :
            if file_name != "":
                with open(file_name, 'w') as f:
                    #For each element in the saved list:
                    for element in saved_items:
                        f.write(element+"\n") #Add it in the file

            #SAVING THE ELEMENTS AND UPDATING THEIR COUNTER
            for element in saved_items:
                #Also add one to the index of each element
                line = element.replace("\"","")
                #Get the index of the line where there is this element, in the initial list of terms
                index_element = list(self.list_autocompletion).index(line)
                #print(list(self.list_autocompletion).index(line)) #to check
                self.list_autocompletion

                #Then update the specific file, based on the choosen language
                #We didn't do both files, bc they are not the same number of lines
                #Bc our method is based on the line index, we can't do both
                if self.language == "FR":
                    self.update_file_content(index_element, "HPO_FR.txt")
                else:
                    self.update_file_content(index_element, "HPO_EN.txt")

            #Then we refresh the completer based on the language of the app
            self.set_autocompleter(self.language)

            #If the answer is yes, we empty the list
            if question_export == QMessageBox.Yes:
                #print("Yes")
                self.listWidget.clear()
            

        else:
            #If here : nothing is in the list, so we show an error message

            self.label_warning2.show() #Display error message 

            #Show custom text depending on error (item already in the saved list)
            if self.language=="FR" :
                self.label_warning2.setText("ERREUR : Vous ne pouvez pas exporter une liste vide.")
            else:
                self.label_warning2.setText("ERROR: You cannot export an empty list.")



    #@pyqtSlot()
    def update_file_content(self, index_element, file_name): 
        #EDIT THE INDEX HERE
        with open(file_name,'r', encoding="utf-8") as txt:
            file_content=txt.readlines() #Save every line of the file in a variable
            old_line = re.split('#', file_content[index_element]) #Get the line of the specific element to be updated
            updated_counter=int(old_line[0])+1 #Add a one to the counter of this element
            updated_line = str(updated_counter)+"#"+old_line[1]+"#\n"#Remake the line with the new counter
            #print(updated_line) #Check if the updated line is correct

            file_content[index_element]=updated_line #Update the line based on the element index
            #print(file_content[index_element]) #Check if line correctly updated

            #Sort the content, to make the searched ones at the top
            file_sorted = sorted(file_content, reverse=True)
            
            #Then we rewrite the file with the updated content : 
            with open(file_name,'w', encoding="utf-8") as txt:
                txt.writelines("_"+line for line in file_sorted)

        #However, we had problems with a specific line : Anomalie de la suture métopique
        #It kept going on the same line of another phenotype, so to prevent this
        #We created a check to see if there is "#_" in the file,
        #If so it indicates that two phenotype are on the same line :
        #_0#Phenotype 1 HPO:0001#_0#Phenotype 2 HPO:0002#
        #(prevent problems or blockage of the program)

        #Open the file, and save its content
        with open(file_name,'r', encoding="utf-8") as txt:
            file_content=txt.read() 
        
        #Replace the "#_" by a "#\n" (it will put the second phenotype on another line)
        file_corrected = file_content.replace('#_', '#\n')

        #Then change also the "_" at the start of every line:
        file_corrected = file_content.replace('_', '')
        
        #Now we can save the corrected content in the initial file by rewriting it
        with open(file_name, 'w', encoding="utf-8") as file:
            file.write(file_corrected)


    @pyqtSlot()
    def on_englishButton_clicked(self):
        if self.listWidget.count() != 0 :
            msg= QMessageBox()
            msg.setText("Attention, cette liste va être vidée !\nBe careful, the list will be emptied!")
            msg.exec()
        
        #Changing the interface language to FRENCH
        self.language = "EN"
        
        #Translation of all elements: ENGLISH version
        self.label_langue.setText('Please choose a language:')
        self.label_aide.setText('In the Phen2HPO interface, you can: \n\n --> Choose the language using the "Language" section.\n\n --> Enter one or more phenotypes using the "Phenotype entry" section. Also, it is possible to delete a phenotype by selecting it and clicking on the "Delete selected element" button. \n\n --> It is also possible to save this list in .csv format using the "Save" button. \n\n\n You can find more detailed information in the user manual present in the folder with the application executable.')
        self.label_aide.setWordWrap(True)
        self.label_1.setText('Please select a phenotype:')
        self.label_2.setText('Patients phenotype list:')

        self.addButton.setText('✓ Add')
        self.deleteButton.setText('✗ Delete the selected element')
        self.exportButton.setText('Export ❯❯')

        self.tabWidget.setTabText(0,'Phenotype entry')
        self.tabWidget.setTabText(1,'Help')
        self.tabWidget.setTabText(2,'Language')

        self.label_warning.setText('') #warning for the input
        self.label_warning2.setText('') #warning for the listview
        self.lineEdit.setText('') #set the input clear

        self.listWidget.clear() #Removes all the element in the list
        #We remove all the element in the list, bc there are not the same
        #amount of lines in the french and the english file
        #Example, if a line in the french file is not present in the english file
        #There will be an error, because the comparison method is by comparind indexes

        self.set_autocompleter(self.language)
        self.reset_list_language(self.language)

    @pyqtSlot()
    def on_francaisButton_clicked(self):
        if self.listWidget.count() != 0 :
            msg= QMessageBox()
            msg.setText("Attention, cette liste va être vidée !\nBecarefull, the list will be emptied!")
            msg.exec()
        #Changing the interface language to FRENCH
        self.language = "FR"
        #Translation of all elements: FRENCH version
        self.label_langue.setText('Veuillez choisir la langue de l\'application :')
        self.label_aide.setText('Dans l\'interface Phen2HPO, vous pouvez : \n\n --> Choisir la langue grâce à la rubrique "Langue".\n\n --> Saisir un ou plusieurs phénotypes grâce à la rubrique "Saisie phénotype". Également, il est possible d\'effacer un phénotype en le sélectionnant et en cliquant sur le bouton "Supprimer l\'élément sélectionné". \n\n --> Il est également possible d\'enregistrer cette liste au format .csv grâce au bouton "Enregistrer". \n\n\n Vous pouvez retrouver des informations plus détaillées dans le manuel utilisateur présent dans le dossier avec l\'exécutable de l\'application.')
        self.label_aide.setWordWrap(True)
        self.label_1.setText('Veuillez saisir un phénotype :')
        self.label_2.setText('Liste des phénotypes du patient :')

        self.addButton.setText('✓ Ajouter')
        self.deleteButton.setText('✗ Supprimer l\'élément sélectionné')
        self.exportButton.setText('Enregistrer ❯❯')

        self.tabWidget.setTabText(0,'Saisie phénotype')
        self.tabWidget.setTabText(1,'Aide')
        self.tabWidget.setTabText(2,'Langue')

        self.label_warning.setText('') #warning for the input
        self.label_warning2.setText('') #warning for the listview
        self.lineEdit.setText('') #set the input clear

        self.listWidget.clear() #Removes all the element in the list
        #Same explanation as in the on_englishButton_clicked(self) method

        self.set_autocompleter(self.language)
        self.reset_list_language(self.language)

    @pyqtSlot()
    def set_autocompleter(self, string):
        #Check which language is chosen:
        if string=="FR":
            nom_fichier="HPO_FR.txt" #French language chosen, use the file with French terms
            #print('Fichier en FR utiliser pour le completer') #Check
        else:
            nom_fichier="HPO_EN.txt" #English language chosen, use the file with English terms
            #print('Fichier en EN utiliser pour le completer') #Check

        #================= FOR THE AUTO-COMPLETION =====================================================================#
        #Create terms list that will be suggested to the user:
        fichier_HPO = codecs.open(nom_fichier, encoding='utf-8') #define file and accept accents with 'utf-8'
        self.index, self.list_autocompletion, trash = loadtxt(fichier_HPO, dtype=str, comments="$", delimiter="#", unpack=True)
        
        #Create the 'completer' linked to the suggestions terms list:
        self.completer = QCompleter(self.list_autocompletion)
        #Initialization of the filter mode for suggestions
        #Here 'MatchContains' allows to suggest all the lines containing the output, regardless of its position in the line
        #For example, if we enter "sco" in FR, it will return "Scotome", "Scoliose", "Faible score APGAR", ...
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)

        #No difference between upper and lower case
        #For example, if we enter "sco" in FR, this can still return the term "Scoliosis" (which starts with a capital letter)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        #Attaching the completer to the inpu (lineEdit) and activating it
        self.completer.setWidget(self.lineEdit)
        self.lineEdit.textChanged.connect(self.handleTextChanged)
        self.completer.activated.connect(self.handleTextChanged)
        self.completer.activated.connect(self.handleCompletion) #Set a custom completion handle
                            
    @pyqtSlot()
    def reset_list_language(self, string):
        #Verify the language chosen, to set up the good terms:
        if string=="FR":
            #Before clicking on the button, it was in English
            #The user wants it in French from now on
            fichier_langue_apres="HPO_FR.txt" 
            #print('FR') #Check

        else:
            #before clicking on the button, it was in French
            #the user wants it in English from now on
            fichier_langue_apres="HPO_EN.txt" 
            #print('EN') #Check
        
        #Create phen/HPO terms list:
        fichier_HPO = codecs.open(fichier_langue_apres, encoding='utf-8') #define file and accept accents with 'utf-8'
        self.index, self.liste_termes, trash = loadtxt(fichier_HPO, dtype=str, comments="$", delimiter="#", unpack=True)
        
        #For each term in the list:
        for index in range(self.listWidget.count()):
            ligne = self.listWidget.item(index).text().split() #fetch the text splitted
            #for example, we will have : ['Anomalie', 'de', 'la', 'taille', 'corporelle', 'HP:0000002']
            
            # ligne[-1] : -1 to have the last item, it will always be the term HPO
            
            matching = [s for s in self.liste_termes if ligne[-1] in s]
            self.listWidget.item(index).setText(str(matching[0]))
            #print(matching) #Check


    #Method based on the following websites:
    #https://stackoverflow.com/questions/16158715/globbing-input-with-qcompleter
    #https://stackoverflow.com/questions/74189826/how-to-achieve-autocomplete-on-a-substring-of-qlineedit-in-pyqt6 
    #https://stackoverflow.com/questions/11401367/pyqt-lineedit-with-readline-completer 
    @pyqtSlot(str)
    def handleTextChanged(self, text):
        #First of all, we check if the last two characters are spaces
        #Because it blocks the app if they are not managed
        if len(text) > 1:
            if text[-1]==" " and text[-2]==" ":
                text=text[:-1]
                self.lineEdit.setText(text)
        
        #Manage if the first character entered is a space
        if len(text) == 1 and text[0]==" ":
            self.lineEdit.setText("")

        #Boolean to check if the element has been found
        found = False

        if len(text) >= 1:
            self.completer.setCompletionPrefix(text)
            
            if self.completer.currentRow() >= 0:
                #Then the prefix is found is one of the elements in the completer
                found = True
                
            else:
                #If input not found, then signal [-1] retrieved
                #It is probably a word with an error or unknown
                
                #We put a minimum length of 2 characters
                #Because otherwise the "find_near_matches" function will crash
                #For example: there is a block if you "dz" by mistake
                if len(text) > 2:
                    #fichier="HPO_FR.txt"
                    
                    #We take the terms in the list :
                    liste_str='\n'.join(self.liste_termes)
                
                    text = text.replace(" ", "_" )
                    liste_str = liste_str.replace(" ", "_" )

                    #print(liste_str) #Check if the list is correct
                    near_matches = find_near_matches(text, liste_str, max_l_dist=1)
                
                    #If the last character entered is a space (indicated by "_"), 
                    #Then we correct the word in the input because otherwise there are no more suggestions
                    if(text[-1]=="_"):
                        if len(near_matches) != 0:
                            self.lineEdit.setText(near_matches[0].matched.replace("_", " " ))
                    
                    #If the list isn't empty, then there is a matching item
                    #to the input, it is therefore necessary to propose it in the completer
                    if len(near_matches) != 0:
                        near_matches[0].dist
                        #print(near_matches[0].matched)

                        self.completer.setCompletionPrefix(near_matches[0].matched.replace("_", " " ))
                        
                        if self.completer.currentRow() >= 0:
                            found = True
                            #print("Found thx to the modif")
                            #print(self.completer.currentCompletion())
                    #else:
                        #If the list is empty, there is no match found
                        #print("Finally not found")

            if found:
                self.completer.complete()
            else:
                self.completer.popup().hide() 

    #METHOD TO MANAGE AUTOCOMPLETION
    #Without this method, there will be no autocompletion when you click on an element of the completer
    @pyqtSlot(str)
    def handleCompletion(self, text):
        prefix = self.completer.completionPrefix()
        self.lineEdit.setText(self.lineEdit.text()[:-len(prefix)] + text)

app=QApplication(sys.argv)
widget=fenetre()
widget.show()

sys.exit(app.exec_())