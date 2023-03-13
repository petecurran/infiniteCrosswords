# Creates crosswords on any topic using the openAI API.
# Pete Curran, 2023

# Import deepcopy to make copies of lists
from copy import deepcopy
from random import choice

# Test data - a list of words from FFVIII
testWords = [
    'SQUALL', 'BALAMB', 'SHIVA', 'ULTIMECIA', 'GUNBLADE', 'DOLLET', 'SEED',
    'SEIFER', 'ADEL', 'GALBADIA', 'JUNCTION', 'AIRSHIP', 'TIMECOMPRESSION',
    'RINOA', 'CIDKRAMER', 'ZELL', 'ESTHAR', 'IRVINE', 'TRIPLE', 'PUZZLEBOSS'
]

# Curated test data
curatedWords = ["BAGEL", "LINGER"]

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
for word in curatedWords:
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

            # Randomly choose a direction for the word
            #wordObject.direction = choice['horizontal', 'vertical']
            wordObject.direction = 'horizontal' #Testing

            # If the word is horizontal:
            if wordObject.direction == 'horizontal':
                # Set the width to the length of the word
                self.width = len(wordObject.text)

                # Set the height to 1 as we only have one word
                self.height = 1

                # Add the word to the grid as a list of characters
                self.grid.append(list(wordObject.text))
            
            # If the word is vertical:
            else:
                # Set the width to 1 as we only have one word
                self.width = 1

                # Set the height to the length of the word
                self.height = len(wordObject.text)

                # Add the word to the grid as a list of characters
                for letter in wordObject.text:
                    self.grid.append([letter])

            # Increment the number of words
            self.numWords += 1

            # Add the word to the list of words added
            self.wordsAdded.append(wordObject)

            # Update the position of the word in the grid
            wordObject.xposition = 0
            wordObject.yposition = 0

            # Return true to indicate that the word was added
            return True
        
        # If this is not the first word to be added:
        else:

            # Find all of the possible intersections between this word and the words already in the grid
            for existingWordObject in self.wordsAdded:
                intersections = self.findIntersections(wordObject, existingWordObject)
                print(intersections)

                # If there are no intersections, return false to indicate that the word was not added
                if len(intersections) == 0:
                    return False
                
                # If there are intersections, try to add the word to the grid
                else:

                    # If the existing word is horizontal:
                    if existingWordObject.direction == 'horizontal':

                        # Set this word to be vertical
                        wordObject.direction = 'vertical'

                        # If the height of the grid is less than the length of the word, increase the height of the grid                        
                        if self.height < len(wordObject.text):
                            oldHeight = self.height
                            self.height = len(wordObject.text)
                            for i in range(self.height - oldHeight):
                                self.grid.append([' ' for i in range(self.width)])



                        # Attempt all possible positions for the word
                        for intersection in intersections:
                            # Set the x position to the x position of the intersection + the x position of the existing word
                            wordObject.xposition = intersection[0] + existingWordObject.xposition

                            # If the y position of the word is less than the y position of the intersection:
                            if existingWordObject.yposition < intersection[1]:
                                
                                # Calculate number of moves down required to get to the intersection
                                movesNeeded = intersection[1] - existingWordObject.yposition

                                # Add the number of extra rows needed to the grid
                                for i in range(movesNeeded):
                                    self.grid.append([' ' for i in range(self.width)])

                                # Move all existing rows down by the number of moves needed
                                for i in range(self.height-1, 0, -1):
                                    self.grid[i] = self.grid[i-1]
                                    
                                # Handle the final row
                                self.grid[0] = [' ' for i in range(self.width)]

                                # Add the word to the grid
                                for letter in range(len(wordObject.text)):
                                    self.grid[letter][wordObject.xposition] = wordObject.text[letter]

                                # Update the position of the word in the grid
                                wordObject.yposition = 0

                                # Increment the number of words
                                self.numWords += 1

                                # Add the word to the list of words added
                                self.wordsAdded.append(wordObject.text)

                                # Return true to indicate that the word was added
                                return True
                                    

    # Tool to look for intersections between words
    def findIntersections(self, word1, word2):          
        # Find all of the possible intersections between letters in the two words
        intersections = []
        for wordOneLetter in range(len(word1.text)):
            for wordTwoLetter in range(len(word2.text)):
                if word1.text[wordOneLetter] == word2.text[wordTwoLetter]:
                    intersections.append((wordOneLetter, wordTwoLetter))
        
        # Return the list of intersections
        return intersections

    
# TODO - The find intersections function is misunderstood.
# Currently I'm treating it like co-ordinates, but it's actually
# (letter in word 1, letter in word 2)
# So intersection (0, 4) means that the first letter in word 1
# is the same as the fifth letter in word 2
# L from linger, L from bagel
# Need to recalculate how to place text in the grid







testCwd = Crossword([], wordsToInclude, 0, 0, 0, 0, [])
# Add the first word from the crossword object to the grid
#testCwd.addWord(testCwd.wordList[0])
#testCwd.addWord(testCwd.wordList[1])
#for row in testCwd.grid:
    #print(row)




    
