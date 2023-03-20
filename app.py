# Import the crossword class from crossword_generator
from crossword_generator import CrosswordGenerator
# Import the config file
import config
# Import the openai library
import openai

# Get the openai key from config.py
openai.api_key = config.openAIKey

theme = input("What is the theme of the crossword?\n")

# Test the openai call
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"system","content":"""You are a clever crossword generator. You are generating crossword clues.
        You aim to choose only words that closely relate to the topic given. It's good if some letters in the words are the same so they can overlap.
        Make sure you provide complete words.
        When you provide respond to the user you should provide a list of words and clues.
        You should use a specific format for the clues: First the number of letters in the word, then "word: ", then the word, then "clue:" then the clue. Put a single space between each one.
        If the word would have a space in it, you should replace the space with a hyphen. For example if the word is 'old man' you should return 'old-man'.
        An Example line would be "5 word: CLOUD clue: The main character in Final Fantasy VII".""
        """},
        {"role":"user","content":"""I want you to generate a list of 10 clues for a crossword puzzle.
        Return the list as a single string, with each clue on a new line."""},
        {"role":"user","content":"The topic for this crossword is '{}'.".format(theme)}
    ])

'''
testWords = [
    'SQUALL', 'BALAMB', 'SHIVA', 'ULTIMECIA', 'GUNBLADE', 'DOLLET', 'SEED',
    'SEIFER', 'GALBADIA', 'JUNCTION', 'AIRSHIP', 'TIMECOMPRESSION',
    'RINOA', 'CIDKRAMER', 'ZELL', 'ESTHAR', 'IRVINE', 'TRIPLE', 'PUZZLEBOSS'
]

# Create a crossword generator object
generator = CrosswordGenerator(testWords, 2)
crossword = generator.generateCrossword()
crossword.printGrid()

print(config.temp)
'''

print(response)
print(response.choices[0].message.content)

# Turn the response into a list
responseList = response.choices[0].message.content.splitlines()
for line in responseList:
    print(line)