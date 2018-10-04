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
        kanjiCount =+ 1

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
