#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from kanji_classes import word
from kanji_classes import kanjiData
from kanji_classes import quizz

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
        #master.bind('1', self.presentQuizz)
        #master.bind('<space>', self.check)
        master.bind('<Escape>', self.client_exit)
        #master.bind('g', self.passQuizz)
        #master.bind('f', self.failQuizz)
        
        self.quizzCount = 0
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

        self.goodButton = Button(self, text = "Good(g)", command = self.passQuizz)
        self.failButton = Button(self, text = "Fail(f)", command = self.failQuizz)
        self.checkButton = Button(self, text = "check(space)", command = self.check)
        self.presentQuizz()

    def init_window(self):
        self.master.title("GUI") #changes title
        self.pack(fill=BOTH,expand = 1)#uses full space of root window
        menu = Menu(self.master)
        self.master.config(menu = menu)
        file = Menu(menu)
        file.add_command(label="Exit",command=self.client_exit)
        menu.add_cascade(label="File",menu=file)
        edit =Menu(menu)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)
        
        quitButton = Button(self, text="Quit(esc)", command = self.client_exit)
        quitButton.place(x=0,y=0)
        
    def client_exit(self, event=None):
        quizzer.outputFile('dummy.csv')
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
        stats = "Remaining Kanji:  " + str(quizzer.getNumberKanjiWithQuizzesRemining()) 
        stats += "/" + str(quizzer.getNumberOriginalKanji()) + "\n"
        stats += "Remaining Quizzes:  " + str(quizzer.getNumberQuizzesRemaining()) 
        stats += "/" + str(quizzer.getNumberOriginalQuizzes()) + "\n"
        stats += "Attempted Quizzes:  " + str(self.quizzCount)
        
        self.progressText.set(stats)  #todo expand to more stats
        self.progressTextLabel.place(relx=1.0, rely = 1.0, anchor = SE)
        
    def hideKanji():
        self.kanjiText.set(self.randoWord.getKanji())
        self.kanjiTextLabel.place(relx=0.5, rely = 0.3, anchor = N)
    
    def hideKana():
        self.kanaText.set(self.randoWord.getKana())
        self.kanaTextLabel.place(relx=0.5, rely = 0.5, anchor = N)
        
    def passQuizz(self, event = None): 
        quizzer.decrementWord(self.randoWord)
        quizzer.logPass(self.randoKanji,self.randoWord.getKanji())
        self.presentQuizz()
    
    def failQuizz(self, event = None):
        quizzer.logFail(self.randoKanji,self.randoWord.getKanji())
        self.presentQuizz()

    def presentQuizz(self, event = None):
        self.randoKanji = quizzer.getRandomKanji()
        self.randoWord = quizzer.getRandomWord(self.randoKanji)
        self.showEnglish()
        self.kanjiTextLabel.place_forget()
        self.kanaTextLabel.place_forget()
        self.showProgress()
        self.goodButton.place_forget()
        self.failButton.place_forget()
        self.checkButton.place(relx= 0.5, rely = 0.75, anchor = N)
        self.master.bind('<space>', self.check)
        self.master.unbind('g')
        self.master.unbind('f')

    def check(self, event = None):
        self.showKanji()
        self.showKana()
        self.goodButton.place(relx= 0.75, rely = 0.75, anchor = N)
        self.failButton.place(relx= 0.25, rely = 0.75, anchor = N)
        self.checkButton.place_forget()
        self.master.unbind('<space>')
        self.master.bind('g', self.passQuizz)
        self.master.bind('f', self.failQuizz)
        self.quizzCount += 1

importFileName = 'kanji_list.csv'
if len(sys.argv) > 1:
    importFileName = sys.argv[1]
print(importFileName)
quizzer = quizz(importFileName)

Root = Tk()
Root.geometry("600x300")
#Root.geometry('40x20')
app = Window(Root)
Root.mainloop()

#todo:
#•add progress bar (remaining_quizzes / starting_quizzes)
#•add picture support for words and all the freaking pictures
#•add hint support for words
#•add side display/log (after designing)
#•doxygen!
#•reverse-quiz (kanji -> kana)

#https://stackoverflow.com/questions/1918005/making-python-tkinter-label-widget-update
#check this out for changing binds:  https://stackoverflow.com/questions/6433369/deleting-and-changing-a-tkinter-event-binding