from parseclues import parseClues
from crossword_generator import CrosswordGenerator
import config
import prompts
import openai
import time # For testing

# Get the openai key from config.py
openai.api_key = config.openAIKey

numClues = 40
theme = input("What is the theme of the crossword?\n")

# Test the openai call
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"system","content":prompts.roleOne},
        {"role":"user","content":"Please supply {} clues.".format(str(numClues))},
        {"role":"user","content":"The topic for this crossword is '{}'.".format(theme)}
    ])

print(response)
#print(response.choices[0].message.content)

# Turn the response into a list
responseList = response.choices[0].message.content.splitlines()
for line in responseList:
    print(line)

content = response.choices[0].message.content
clues = parseClues(content)
print(clues)

generatedClues = []

for clue in clues:
    # If there's a hyphen in the clue, remove it.
    if '-' in clue['word']:
        clue['word'] = clue['word'].replace('-', '')
    # If there's a space in the clue, remove it.
    if ' ' in clue['word']:
        clue['word'] = clue['word'].replace(' ', '')
    
    # Add the clue to the list of generated clues
    generatedClues.append(clue['word'])

# Create a crossword generator object

# Start a timer
start = time.time()
generator = CrosswordGenerator(generatedClues, 500)
crossword = generator.generateCrossword()
end = time.time()
# Print the time taken in minutes and seconds
print("Time taken: {} minutes and {} seconds".format(int((end-start)/60), int((end-start)%60)))
crossword.printGrid()
print("Words added: {}".format(crossword.numWords))
print("Intersections: {}".format(crossword.numberOfIntersections))