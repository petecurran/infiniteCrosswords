# Creates crosswords on any topic using the openAI API.
# Pete Curran, 2023

# Import deepcopy to make copies of lists
from copy import deepcopy
from random import choice, shuffle

# Test data - a list of words from FFVIII
testWords = [
    'SQUALL', 'BALAMB', 'SHIVA', 'ULTIMECIA', 'GUNBLADE', 'DOLLET', 'SEED',
    'SEIFER', 'GALBADIA', 'JUNCTION', 'AIRSHIP', 'TIMECOMPRESSION',
    'RINOA', 'CIDKRAMER', 'ZELL', 'ESTHAR', 'IRVINE', 'TRIPLE', 'PUZZLEBOSS'
]

# Test data for alignment
alignTest = ['IRVINE', 'TRIPLE', 'SHIVA', 'CIDKRAMER', 'GUNBLADE', 'ESTHAR', 'TIMECOMPRESSION', 'SEED', 'GALBADIA', 'RINOA', 'ULTIMECIA', 'AIRSHIP', 'ZELL', 'JUNCTION', 'PUZZLEBOSS', 'BALAMB', 'SQUALL', 'SEIFER', 'DOLLET']

# Curated test data
curatedWords = ["ABCD", "GFED", "JIHG", "MAJKKA", "TIX"]

# Generator class
class CrosswordGenerator:
    '''Generates crosswords and returns the best option.'''
    def __init__(self, wordsToInclude, numberOfAttempts):
        self.wordsToInclude = wordsToInclude
        self.numberOfAttempts = numberOfAttempts
        self.words = []
        self.generatedCrosswords = []

    def setUpWords(self):
        for word in self.wordsToInclude:
            # Create a Word object for each word
            self.words.append(Word(word, None, None, None))

    def generateCrossword(self):
        self.setUpWords()
        for i in range(self.numberOfAttempts):
            # Create a new crossword
            attempt = Crossword([], self.words, 0, 0, 0, 0, [])
            # Shuffle the list of words
            shuffle(attempt.wordList)

            # Attempt to add all of the words in the list
            for word in attempt.wordList:
                attempt.addWord(word)
            
            # If there are any words that failed to add, try to add them again
            if attempt.wordsFailedToAdd:
                shuffle(attempt.wordsAdded)
                for word in attempt.wordsFailedToAdd:
                    # Only try to add the word again if it hasn't been attempted 3 times
                    if word.attemptsToAdd < 3:
                        attempt.addWord(word)

            # Add the crossword to the list of generated crosswords
            self.generatedCrosswords.append(attempt)
        
        # Sort the list of generated crosswords by the number of words added
        self.generatedCrosswords.sort(key=lambda x: x.numWords, reverse=True)

        # Testing - print the best 3 crosswords
        '''for i in range(3):
            self.generatedCrosswords[i].printGrid()
            print("Number of words:",self.generatedCrosswords[i].numWords)
            print("~"*50)'''

        return self.generatedCrosswords[0]

# Class to hold words and their positions in the crossword
class Word:
    def __init__(self, text, xposition, yposition, direction):
        self.text = text # The text of the word
        self.clueNumber = None # The number of the clue for the word
        self.xposition = xposition # The x position of the first letter of the word
        self.yposition = yposition # The y position of the first letter of the word
        self.direction = direction # The direction of the word - 'horizontal' or 'vertical'
        self.length = len(text)
        self.storedxposition = xposition # Store the original x position so we can reset it if the word fails to add
        self.storedyposition = yposition # Store the original y position so we can reset it if the word fails to add
        self.attemptsToAdd = 0 # Number of times the word has been attempted to be added

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
        self.wordsFailedToAdd = []

    def checkOverlaps(self, wordObject, intersectionIndex):
        '''Check if the word overlaps any existing words in the grid.
        Returns true if the word doesn't overlap any existing words, or if the overlapping letters match.
        Returns false otherwise.'''

        # Record the index of letters that overlap with existing letters
        overlappingIndexes = [intersectionIndex]

        # Check if the word overlaps any existing words in the grid
        # If the word is horizontal:
        if wordObject.direction == 'horizontal':
            for i in range(wordObject.length):
                # Check if the letter in the word overlaps with an existing letter that doesn't match the letter in the word
                if self.grid[wordObject.yposition][wordObject.xposition + i] != '' and self.grid[wordObject.yposition][wordObject.xposition + i] != wordObject.text[i]:
                    return False

                # Create a list of indexes that overlap with existing letters, excluding the index of the intersection
                if self.grid[wordObject.yposition][wordObject.xposition + i] == wordObject.text[i] and i != intersectionIndex:
                    overlappingIndexes.append(i)

            # Check if the word overlaps with other characters to create invalid words.
            # If the word is not on the final row, check the row below for overlapping letters
            if wordObject.yposition < self.height - 1:
                for i in range(wordObject.length):
                    if self.grid[wordObject.yposition + 1][wordObject.xposition + i] != '' and i not in overlappingIndexes:
                        return False
                    
            # If the word is not on the first row, check the row above for overlapping letters
            if wordObject.yposition > 0:
                for i in range(wordObject.length):
                    if self.grid[wordObject.yposition - 1][wordObject.xposition + i] != '' and i not in overlappingIndexes:
                        return False
                    
            # If the word does not begin in the first column, check the column to the left for overlapping letters
            if wordObject.xposition > 0:
                if self.grid[wordObject.yposition][wordObject.xposition - 1] != '':
                    return False
            
            # If the word does not end in the last column, check the column to the right for overlapping letters
            if wordObject.xposition + wordObject.length < self.width:
                if self.grid[wordObject.yposition][wordObject.xposition + wordObject.length] != '':
                    return False

        # If the word is vertical:
        else:
            for i in range(wordObject.length):
                # Check if the letter in the word overlaps with an existing letter that doesn't match the letter in the word
                if self.grid[wordObject.yposition + i][wordObject.xposition] != '' and self.grid[wordObject.yposition + i][wordObject.xposition] != wordObject.text[i]:
                    return False
                
                # Create a list of indexes that overlap with existing letters, excluding the index of the intersection
                if self.grid[wordObject.yposition + i][wordObject.xposition] == wordObject.text[i] and i != intersectionIndex:
                    overlappingIndexes.append(i)

                # Check if the word overlaps with other characters to create invalid words.
                # If the word is not on the final column, check the column to the right for overlapping letters
                if wordObject.xposition < self.width - 1:
                    for i in range(wordObject.length):
                        if self.grid[wordObject.yposition + i][wordObject.xposition + 1] != '' and i not in overlappingIndexes:
                            return False
                
                # If the word is not on the first column, check the column to the left for overlapping letters
                if wordObject.xposition > 0:
                    for i in range(wordObject.length):
                        if self.grid[wordObject.yposition + i][wordObject.xposition - 1] != '' and i not in overlappingIndexes:
                            return False
                
                # If the word does not begin in the first row, check the row above for overlapping letters
                if wordObject.yposition > 0:
                    if self.grid[wordObject.yposition - 1][wordObject.xposition] != '':
                        return False
                
                # If the word does not end in the last row, check the row below for overlapping letters
                if wordObject.yposition + wordObject.length < self.height:
                    if self.grid[wordObject.yposition + wordObject.length][wordObject.xposition] != '':
                        return False

        # If the word doesn't overlap any existing words, or if the overlapping letters match, return true
        return True
                

    # Add a word to the crossword
    def addWord(self, wordObject):
        '''Add a word to the crossword.
        Returns true if the word was added, or false if the word could not be added.'''

        # If this is the first word to be added:
        if self.currentIndex == 0:

            # Randomly choose a direction for the word
            wordObject.direction = choice(['horizontal', 'vertical'])
            #wordObject.direction = 'horizontal' #Testing

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

            # Increment the current index
            self.currentIndex += 1

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
                
                # Testing - print the intersections
                #print(intersections)

                # If there are no intersections, continue to try the next word
                if len(intersections) == 0:
                    continue
                
                # If there are intersections, try to add the word to the grid
                else:

                    # Backup the key variables in case we need to revert to the previous state
                    # Create a deep copy of the grid
                    gridCopy = deepcopy(self.grid)

                    # Create copies of the width and height
                    widthCopy = self.width
                    heightCopy = self.height

                    # Backup the current position of the existing word
                    existingWordXPosition = existingWordObject.xposition
                    existingWordYPosition = existingWordObject.yposition

                    # Backup the position of all of the previous words in case we need to revert to the previous state
                    for word in self.wordsAdded:
                        word.storedxposition = word.xposition
                        word.storedyposition = word.yposition

                    # If the existing word is horizontal:
                    if existingWordObject.direction == 'horizontal':

                        # Set this word to be vertical
                        wordObject.direction = 'vertical'

                        # Attempt all possible positions for the word
                        for intersection in intersections:
                            # Set the x position to the x position of the intersection + the x position of the existing word
                            wordObject.xposition = intersection[1] + existingWordObject.xposition

                            # Set the y position of the word object to 0 in case it was set to a different value in a previous iteration
                            wordObject.yposition = 0

                            # If the intersection is at the start of the word, set the y position to the y position of the existing word
                            if intersection[0] == 0:
                                wordObject.yposition = existingWordObject.yposition

                            # Otherwise, check if we need to move the grid down to make room for the word
                            else:
                                # If the y position of the existing word is lower than the intersection with the second word,
                                # We need to move the grid down to make room for the word
                                if existingWordObject.yposition < intersection [0]: 
                                    
                                    # Calculate the number of rows we need to move the grid down
                                    rowsToMove = intersection[0] - existingWordObject.yposition

                                    # Add the required number of rows to the grid
                                    for row in range(rowsToMove):
                                        self.grid.append([''] * self.width)

                                    # Update the height of the grid
                                    self.height += rowsToMove

                                    # Move each existing row down
                                    # TODO - This could be done more efficiently
                                    for i in range(rowsToMove):
                                        for row in range(self.height-1, -1, -1):
                                            # Append an empty row to the top of the grid
                                            if row == 0:
                                                self.grid[row] = [''] * self.width
                                            # Move each row down one
                                            else:
                                                self.grid[row] = self.grid[row-1]

                                    # Update the y position of all existing words
                                    for word in self.wordsAdded:
                                        word.yposition += rowsToMove

                                    # Update the y position of the word
                                    wordObject.yposition = 0

                                # Otherwise, calculate the y position of the word using the intersection.
                                else:
                                    wordObject.yposition = existingWordObject.yposition - intersection[0] # This line was causing the vertical words to misalign

                            # Check if we need to make the grid taller to make room for the new word
                            if wordObject.yposition + wordObject.length > self.height:
                                # Calculate the number of rows we need to add to the grid
                                rowsToAdd = wordObject.yposition + wordObject.length - self.height

                                # Add the required number of rows to the grid
                                for row in range(rowsToAdd):
                                    self.grid.append([''] * self.width)

                                # Update the height of the grid
                                self.height += rowsToAdd

                            # Check overlap with existing words
                            # If the overlap is valid, add the word to the grid
                            # Sends the index of the new word's intersection with the old word.
                            if self.checkOverlaps(wordObject, intersection[0]):

                                # Write the word to the grid
                                for i in range(wordObject.length):
                                    self.grid[wordObject.yposition + i][wordObject.xposition] = wordObject.text[i]

                                # Add the word to the list of words added
                                self.wordsAdded.append(wordObject)

                                # Increment the number of words
                                self.numWords += 1

                                # Increment the current index
                                self.currentIndex += 1
                            
                                # Return true to indicate that the word was added
                                return True
                            
                            # If the overlap is not valid, reset the grid and try the next position
                            else:
                                self.grid = deepcopy(gridCopy)
                                self.width = widthCopy
                                self.height = heightCopy
                                existingWordObject.xposition = existingWordXPosition
                                existingWordObject.yposition = existingWordYPosition
                                for word in self.wordsAdded:
                                    word.yposition = word.storedyposition

                    # If the existing word is vertical:
                    else:
                            
                        # Set this word to be horizontal
                        wordObject.direction = 'horizontal'

                        # Attempt all possible positions for the word
                        for intersection in intersections:
                            # Set the y position to the y position of the intersection + the y position of the existing word
                            wordObject.yposition = intersection[1] + existingWordObject.yposition

                            # Set the x position to 0 in case it was set to a value in the previous iteration
                            wordObject.xposition = 0

                            # If the intersection is at the start of the word, set the x position to the x position of the existing word
                            if intersection[0] == 0:
                                wordObject.xposition = existingWordObject.xposition

                            # Otherwise, check if we need to move the grid right to make room for the word
                            else:
                                # If the x position of the existing word is lower than the intersection with the second word,
                                # We need to move the grid right to make room for the word
                                if existingWordObject.xposition < intersection [0]:
                                    
                                    # Calculate the number of columns we need to move the grid right
                                    columnsToMove = intersection[0] - existingWordObject.xposition

                                    # Move each existing column right
                                    # TODO - This could be done more efficiently
                                    for i in range(columnsToMove):
                                        for row in range(self.height):
                                            # Append an empty column to the left of the grid
                                            self.grid[row].insert(0, '')

                                    # Update the width of the grid
                                    self.width += columnsToMove

                                    # Update the x position of all existing words
                                    for word in self.wordsAdded:
                                        word.xposition += columnsToMove

                                    # Update the x position of the word
                                    wordObject.xposition = 0

                                # Otherwise, calculate the x position of the word using the intersection.
                                else:
                                    wordObject.xposition = existingWordObject.xposition - intersection[0]

                            # Check if we need to make the grid wider to make room for the new word
                            if wordObject.xposition + wordObject.length > self.width:
                                # Calculate the number of columns we need to add to the grid
                                columnsToAdd = wordObject.xposition + wordObject.length - self.width

                                # Add the required number of columns to the grid
                                for row in range(self.height):
                                    for column in range(columnsToAdd):
                                        self.grid[row].append('')

                                # Update the width of the grid
                                self.width += columnsToAdd

                            # Check overlap with existing words
                            # If the overlap is valid, add the word to the grid
                            # Sends the index of the new word's intersection with the old word.
                            if self.checkOverlaps(wordObject, intersection[0]):

                                # Write the word to the grid
                                for i in range(wordObject.length):
                                    self.grid[wordObject.yposition][wordObject.xposition + i] = wordObject.text[i]

                                # Add the word to the list of words added
                                self.wordsAdded.append(wordObject)

                                # Increment the number of words
                                self.numWords += 1

                                # Increment the current index
                                self.currentIndex += 1

                                # Return true to indicate that the word was added
                                return True

                            # If the overlap is not valid, reset the grid and try the next position
                            else:
                                self.grid = deepcopy(gridCopy)
                                self.width = widthCopy
                                self.height = heightCopy
                                existingWordObject.xposition = existingWordXPosition
                                existingWordObject.yposition = existingWordYPosition

                                for word in self.wordsAdded:
                                    word.xposition = word.storedxposition

        # If no valid positions were found, increment the attempts on the word and add it to the list of words that failed to add
        wordObject.attemptsToAdd += 1        
        self.wordsFailedToAdd.append(wordObject)
        return False
                             
    # Tool to look for intersections between words
    def findIntersections(self, word1, word2):
        '''Find all of the possible intersections between two words
        Returns a list of tuples, each tuple containing the position of the intersection in each word
        The first element in the tuple is the position in word1, the second element is the position in word2.
        Under normal use this is (Position in the new word, position in the existing word)'''

        # Validation - Check that the words are in different directions
        if word1.direction == word2.direction:
            return []

        # Find all of the possible intersections between letters in the two words
        intersections = []
        for wordOneLetter in range(len(word1.text)):
            for wordTwoLetter in range(len(word2.text)):
                if word1.text[wordOneLetter] == word2.text[wordTwoLetter]:
                    intersections.append((wordOneLetter, wordTwoLetter))
        
        # Return the list of intersections
        return intersections

    # Tool to assign clue numbers to wordsAdded
    def assignClueNumbers(self):
        '''Assigns clue numbers to the words successfully added.
        Traverses the grid from left to right, top to bottom.
        Starts at 1 and increments by 1 for each word added.
        Horizontal and vertical clues with the same coordinates are assigned the same clue number.'''

        # Set the clue number to 0
        clueNumber = 0

        # Sort the wordsAdded list by y position, then by x position, then by direction with horizontal words first
        self.wordsAdded.sort(key=lambda word: (word.yposition, word.xposition, word.direction == 'horizontal'), reverse=False)

        # Variable to store the last y and x positions so we can handle words with the same coordinates
        lastYPosition = -1
        lastXPosition = -1

        # Assign clue numbers to the words, in order.
        for word in self.wordsAdded:

            # If the word is at the same coordinates as the last word, assign it the same clue number
            if word.yposition == lastYPosition and word.xposition == lastXPosition:
                word.clueNumber = clueNumber
            
            else:
                # Increment the clue number
                clueNumber += 1

                # Assign the clue number to the word
                word.clueNumber = clueNumber

            # Update the last y and x positions
            lastYPosition = word.yposition
            lastXPosition = word.xposition

        # Testing - print the x and y positions of the wordsAdded list
        '''for word in self.wordsAdded:
            print(word.clueNumber, word.text, word.yposition, word.xposition)'''


    # Print the grid
    def printGrid(self):
        for row in self.grid:
            for col in row:
                if col == '':
                    print (' ', end=' ')
                else:
                    print(col, end=' ')
            print()

### TESTING AREA ###

# Generate a list of Word objects from testWords
#wordsToInclude = []
#for word in alignTest:
#    wordsToInclude.append(Word(word, None, None, None))

# Test method to generate crosswords without generator.
def testCrosswords():

    # A list to hold completed crosswords
    generatedCrosswords = []

    # Choose how many crosswords to generate
    numCrosswords = 20

    # Generate the crosswords
    for i in range(numCrosswords):
        # Create a new crossword object
        attempt = Crossword([], wordsToInclude, 0, 0, 0, 0, [])

        # Shuffle the list of words
        shuffle (attempt.wordList)

        # Attempt to add all of the words in the list
        for word in attempt.wordList:
            attempt.addWord(word)

        # Add the completed crossword to the list of generated crosswords
        generatedCrosswords.append(attempt)

    # Sort the crosswords by number of words, with the most words first
    generatedCrosswords.sort(key=lambda x: x.numWords, reverse=True)

    # Print the three largest crosswords
    for i in range(3):
        generatedCrosswords[i].printGrid()
        print("~"*50)
        print("Number of words:", generatedCrosswords[i].numWords)
        print("~"*50)

# Run the test
#testCrosswords()

# Generate a crossword using the generator
'''
generator = CrosswordGenerator(testWords,20)
result = generator.generateCrossword()
result.printGrid()
result.assignClueNumbers()
print("Best option number of words:",result.numWords)
'''