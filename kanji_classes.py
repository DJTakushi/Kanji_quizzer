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
        print(kanjiData.kanjiCount)

    def addWord(self, inputWord):
        self.kanjiWordList.append(inputWord)
        #print(inputWord.getEnglish())
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
    def __init__(self):
        self.kanjiDict = generateTankList()
        self.Quizzes = self.getNumberQuizzesRemaining()

    #print out evaluation as file
    def outputFile(self):
        outputTankList(self.kanjiDict)

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
            return TRUE
        else    
            return FALSE

    #check if there are words for a given kanji
    #def isWordsforKanji(self,character): 
        #I don't think this is necessary for anything but getRandomKanji, and it only saves a single line there

    #decrement counter for a given kanji
    def dercrementQuizz(self, kanji):
        self.kanjiDict[kanji].decrementRemainingCount()
    
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
        for kanji in self.kanjiDict:
                remaining += self.getQuizzesForKanji(kanji)
        return remaining

    #return number or original kanji
    def getNumberOriginalKanji(self):
        return len(self.kanjiDict)

    #return number of original quizzes
    def getNumberOriginalQuizzes(self):
        return self.Quizzes
#data
 #dictionary
  #key = kanji character
  #value = kanjiData
 #Quizzes(original)
 #RemainingQuizzes
 
 
 #HELPER FUNCTIONS
def generateTankList():
     #import Kanji
    #todo: make the file name be a parameter
    outputDict = {}
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