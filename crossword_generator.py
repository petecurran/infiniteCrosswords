# Creates crosswords on any topic using the openAI API.
# Pete Curran, 2023

# Import deepcopy to make copies of lists
from copy import deepcopy

# Test data - a list of words from FFVIII
testWords = [
    'SQUALL', 'BALAMB', 'SHIVA', 'ULTIMECIA', 'GUNBLADE', 'DOLLET', 'SEED',
    'SEIFER', 'ADEL', 'GALBADIA', 'JUNCTION', 'AIRSHIP', 'TIMECOMPRESSION',
    'RINOA', 'CIDKRAMER', 'ZELL', 'ESTHAR', 'IRVINE', 'TRIPLE', 'PUZZLEBOSS'
]

# A list to hold completed crosswords
generatedCrosswords = []

# Class to hold words and their positions in the crossword
class Word:
    def __init__(self, text, xposition, yposition, direction):
        self.text = text
        self.xposition = xposition
        self.yposition = yposition
        self.direction = direction
        self.length = len(text)

# Generate a list of Word objects from testWords
wordsToInclude = []
for word in testWords:
    wordsToInclude.append(Word(word, None, None, None))

# Crossword class
class Crossword:
    def __init__(self, grid=[], wordList=[], currentIndex=0, numWords=0, width=0, height=0, wordsAdded=[]):
        # Make a copy of the word list
        self.wordList = deepcopy(wordList)
        self.currentIndex = currentIndex
        self.grid = grid
        self.numWords = numWords
        self.width = width
        self.height = height
        self.wordsAdded = wordsAdded

    # Add a word to the crossword
    def addWord(self, wordObject):

        # If this is the first word to be added:
        if self.numWords == 0:

            # Set the width to the length of the word
            self.width = len(wordObject.text)

            # Set the height to 1 as we only have one word
            self.height = 1

            # Add the word to the grid as a list of characters
            self.grid.append(list(wordObject.text))

            # Increment the number of words
            self.numWords += 1

            # Add the word to the list of words added
            self.wordsAdded.append(wordObject.text)

            # Update the position of the word in the grid
            wordObject.xposition = 0
            wordObject.yposition = 0
            wordObject.direction = 'horizontal'

            # Return true to indicate that the word was added
            return True
        

    # Tool to look for intersections between words
    def findIntersections(self, word1, word2):
            
            pass


testCwd = Crossword([], wordsToInclude, 0, 0, 0, 0, [])
# Add the first word from the crossword object to the grid
testCwd.addWord(testCwd.wordList[0])
print(testCwd.grid)


    
