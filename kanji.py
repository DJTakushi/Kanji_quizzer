#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import random
from kanji_classes import word
from kanji_classes import kanjiData

try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self,master)
        self.master = master
        master.bind('1', self.presentQuizz)
        master.bind('<space>', self.check)
        master.bind('<Escape>', self.client_exit)
        master.bind('g', self.passQuizz)
        master.bind('f', self.failQuizz)
        
        self.randoKanji = ''
        self.randoWord = word('','','')
        
        self.init_window()
        self.mainTextFont = ('times',40,'bold')
        self.secondaryTextFont = ('times',10,'bold')

        self.kanjiText = StringVar()
        self.kanjiTextLabel = Label(self,textvariable = self.kanjiText)
        self.kanjiTextLabel.config(font = self.mainTextFont)

        self.englishText = StringVar()
        self.englishTextLabel = Label(self,textvariable = self.englishText)
        self.englishTextLabel.config(font = self.mainTextFont)

        self.kanaText = StringVar()
        self.kanaTextLabel = Label(self,textvariable = self.kanaText)
        self.kanaTextLabel.config(font = self.mainTextFont)
        
        self.progressText = StringVar()
        self.progressTextLabel = Label(self,textvariable = self.progressText)
        self.progressTextLabel.config(font = self.secondaryTextFont)

        self.presentQuizz()

    def init_window(self):
        self.master.title("GUI") #chagnes title
        self.pack(fill=BOTH,expand = 1)#uses full space of root window
        menu = Menu(self.master)
        self.master.config(menu = menu)
        file = Menu(menu)
        file.add_command(label="Exit",command=self.client_exit)
        menu.add_cascade(label="File",menu=file)
        edit =Menu(menu)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)
        
        quitButton = Button(self, text="Quit", command = self.client_exit)
        quitButton.place(x=0,y=0)
        
        passButton = Button(self, text = "passButton", command = self.passQuizz)
        passButton.place(relx= 0.75, rely = 0.65, anchor = N)
        passButton.place_forget()
        
        failButton = Button(self, text = "failButton", command = self.failQuizz)
        failButton.place(relx= 0.25, rely = 0.65, anchor = N)
        failButton.place_forget()

        quizzButton = Button(self, text = "quizzButton", command = self.presentQuizz)
        quizzButton.place(relx= 0.25, rely = 0.75, anchor = N)

        checkButton = Button(self, text = "checkButton", command = self.check)
        checkButton.place(relx= 0.75, rely = 0.75, anchor = N)

    def client_exit(self, event=None):
        outputTankList(KanjiTankDict) 
        exit()
        
    def showEnglish(self):
        self.englishText.set(self.randoWord.getEnglish())
        self.englishTextLabel.place(relx=0.5, rely = 0.1, anchor = N)

    def showKanji(self):
        self.kanjiText.set(self.randoWord.getKanji())
        self.kanjiTextLabel.place(relx=0.5, rely = 0.3, anchor = N)

    def showKana(self):
        self.kanaText.set(self.randoWord.getKana())
        self.kanaTextLabel.place(relx=0.5, rely = 0.5, anchor = N)

    def showProgress(self):
        #self.progressText.set(KanjiTankDict[self.randoKanji].kanjiCount)
        self.progressText.set(kanjiData.kanjiCount)
        self.progressTextLabel.place(relx=1.0, rely = 1.0, anchor = SE)


        
    def hideKanji():
        self.kanjiText.set(self.randoWord.getKanji())
        self.kanjiTextLabel.place(relx=0.5, rely = 0.3, anchor = N)
    
    def hideKana():
        self.kanaText.set(self.randoWord.getKana())
        self.kanaTextLabel.place(relx=0.5, rely = 0.5, anchor = N)
        
    def passQuizz(self, event = None): 
        #self.showText("passQuizz()")
        for character in self.randoWord.getKanji():
            if character in KanjiTankDict:
                #outputDict[character].addWord(thisWord)
                KanjiTankDict[character].decrementRemainingCount()
        self.presentQuizz()
    
    def failQuizz(self, event = None):
        #self.showText("failQuizz()")
        self.presentQuizz()

    def presentQuizz(self, event = None):
        self.randoKanji = random.choice(list(KanjiTankDict))
        while (not KanjiTankDict[self.randoKanji].getWordList()) and (KanjiTankDict[self.randoKanji].getRemainingCount()>0):
            self.randoKanji = random.choice(list(KanjiTankDict))
        self.randoWord = random.choice(KanjiTankDict[self.randoKanji].getWordList())
        self.showEnglish()
        self.kanjiTextLabel.place_forget()
        self.kanaTextLabel.place_forget()
        self.showProgress()

        
    def check(self, event = None):
        self.showKanji()
        self.showKana()

def generateTankList():
    outputDict = {}
    #import Kanji
    with open('kanji_list.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            outputDict[row['kanji']]= kanjiData()
            outputDict[row['kanji']].setRemainingCount(1)

    #import words
    with open('word_list.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            thisWord = word(row['english'],row['kanji'],row['kana'])
            #englishword=thisWord.getEnglish()
            #print(thisWord.getEnglish())
            for character in thisWord.getKanji():
                if character in outputDict:
                    #adds this word to the dictionary's entry for the kanji
                    outputDict[character].addWord(thisWord)
    return outputDict
    
def outputTankList(inputDict):
    f = open("dummy.csv","w+")
    with open('dummy.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #spamwriter.writerow(['Spam'] *5 + ['Baked Beans'])
        #spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        datList = ()
        for key in inputDict:
            if 1:#not inputDict[key].getWordList(): 
                datList = ([key] + [inputDict[key].remainingCount])
                for item in inputDict[key].getWordList():
                    #print(item)
                    datList.append(item.getKanji())
                #spamwriter.writerow([key] + [inputDict[key].remainingCount] + [inputDict[key].getWordList()])
                spamwriter.writerow(datList)
    f.close()


KanjiTankDict = generateTankList()
outputTankList(KanjiTankDict) 




Root = Tk()
Root.geometry("400x300")
app = Window(Root)
Root.mainloop()

#todo:
#•add progress bar (remaining_quizzes / starting_quizzes)
#•check that any passed word decrements the counter for all kanji
#•create option to import a dummy to start from a save point
#•refactor kanjiTankDict as a dedicated structure

#https://stackoverflow.com/questions/1918005/making-python-tkinter-label-widget-update
#check this out for changing binds:  https://stackoverflow.com/questions/6433369/deleting-and-changing-a-tkinter-event-binding