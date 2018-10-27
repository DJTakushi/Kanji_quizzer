import csv
import random

class word:
    def __init__(self, english, kanji, kana):
        self.english = english
        self.Kanji = kanji
        self.Kana = kana
        
    def getEnglish(self):
        return self.english
    
    def getKanji(self):
        return self.Kanji
        
    def getKana(self):
        return self.Kana
    
class kanjiData:
    kanjiCount = 0

    def __init__(self):
        self.remainingCount = 0
        self.kanjiWordList = [] #() may also work
        kanjiData.kanjiCount += 1

    def addWord(self, inputWord):
        self.kanjiWordList.append(inputWord)

    def getWordList(self):
        return self.kanjiWordList
        
    def getRemainingCount(self):
        return(self.remainingCount)

    def setRemainingCount(self,count):
        self.remainingCount = count
    
    def decrementRemainingCount(self):
        self.remainingCount-=1

    def incrementRemainingCount(self):
        self.remainingCount+=1
        
    def getKanjiCount(self):
        return kanjiCount
        
class quizz:
#Functions
    #generate self from given files
    def __init__(self,kanjiFile):
        self.kanjiDict = generateTankList(kanjiFile)
        self.Quizzes = self.getNumberQuizzesRemaining()
        self.log = []

    #print out evaluation as file
    def outputFile(self, fileName):
        outputTankList(self.kanjiDict, fileName)
        outputLog(self.log, "log")

    #return random kanji from dictionary to quizz
    def getRandomKanji(self):
        kanji = random.choice(list(self.kanjiDict))
        while (not self.kanjiDict[kanji].getWordList()) and (self.kanjiDict[kanji].getRemainingCount()>0):
            kanji = random.choice(list(kanjiDict))
        return kanji

    #return random word for a given kanji
    def getRandomWord(self,kanji):
        return random.choice(self.kanjiDict[kanji].getWordList())

    #check if a given character is in the dictionary
    def isKanjiInDict(self,character):
        if character in self.kanjiDict:
            return True
        else:
            return False

    #check if there are words for a given kanji
    #def isWordsforKanji(self,character): 
        #I don't think this is necessary for anything but getRandomKanji, and it only saves a single line there

    #decrement counter for a given kanji - NO LONGER USED
    #def decrementQuizz(self, kanji):
        #self.kanjiDict[kanji].decrementRemainingCount()
    
    #decrements counters for word
    def decrementWord(self,word):
        for character in word.getKanji():
            if self.isKanjiInDict(character):
                self.kanjiDict[character].decrementRemainingCount()
    
    #return quizzes for a given kanji
    def getQuizzesForKanji(self,kanji):
        return self.kanjiDict[kanji].getRemainingCount()

    #return number of kanji with quizzes remaining
    def getNumberKanjiWithQuizzesRemining(self):
        remaining = 0
        for kanji in self.kanjiDict:
            if self.getQuizzesForKanji(kanji):
                remaining += 1
        return remaining

    #return all quizzes remaining
    def getNumberQuizzesRemaining(self):
        remaining = 0
        tempRemaining = 0
        for kanji in self.kanjiDict:
            tempRemaining = self.getQuizzesForKanji(kanji)
            if tempRemaining > 0:#don't count negative counts
                remaining += tempRemaining
        return remaining

    #return number or original kanji
    def getNumberOriginalKanji(self):
        return len(self.kanjiDict)

    #return number of original quizzes
    def getNumberOriginalQuizzes(self):
        return self.Quizzes

    #log results
    def logPass(self,kanji,word):
        self.log.append(("PASS",kanji,word,self.getNumberKanjiWithQuizzesRemining(),self.getNumberQuizzesRemaining()))

    def logFail(self,kanji,word):
        self.log.append(("FAIL",kanji,word,self.getNumberKanjiWithQuizzesRemining(),self.getNumberQuizzesRemaining()))


#data
 #dictionary
  #key = kanji character
  #value = kanjiData
 #Quizzes(original)
 #RemainingQuizzes
 
 
 #HELPER FUNCTIONS
def generateTankList(inputFile):
     #import Kanji
    #todo: make the file name be a parameter
    outputDict = {}
    with open(inputFile, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            outputDict[row['kanji']]= kanjiData()
            outputDict[row['kanji']].setRemainingCount(int(row['count']))

    #import words
    with open('word_list.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            thisWord = word(row['english'],row['kanji'],row['kana'])
            for character in thisWord.getKanji():
                if character in outputDict:
                    #adds this word to the dictionary's entry for the kanji
                    outputDict[character].addWord(thisWord)
    return outputDict

def outputTankList(inputDict, fileName):
    f = open(fileName,"w+")
    with open(fileName, 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #spamwriter.writerow(['Spam'] *5 + ['Baked Beans'])
        #spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        datList = ("kanji","count")
        spamwriter.writerow(datList)        
        for key in inputDict:
            if 1:#not inputDict[key].getWordList(): 
                datList = ([key] + [inputDict[key].remainingCount])
                for item in inputDict[key].getWordList():
                    datList.append(item.getKanji())
                #spamwriter.writerow([key] + [inputDict[key].remainingCount] + [inputDict[key].getWordList()])
                spamwriter.writerow(datList)
    f.close()

def outputLog(logList, fileName):
    f = open(fileName,"w+")
    with open(fileName, 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        datList = ("kanji","word","result")
        spamwriter.writerow(datList)        
        for log in logList:
            spamwriter.writerow(log)
            #spamwriter.writerow(datList)
    f.close()