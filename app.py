from parseclues import parseClues
from crossword_generator import CrosswordGenerator
from print_generator import crosswordPrinter, generateImage
import config
import prompts
import openai
import time # For testing

# Get the openai key from config.py
openai.api_key = config.openAIKey

numClues = 20
theme = input("What is the theme of the crossword?\n")

# Test the openai call
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"system","content":prompts.roleOne},
        {"role":"user","content":"Please supply {} clues.".format(str(numClues))},
        {"role":"user","content":"The topic for this crossword is '{}'.".format(theme)}
    ])

content = response.choices[0].message.content
clues = parseClues(content)
print(clues)

# Start a timer
start = time.time()
generator = CrosswordGenerator(clues, 20)
crossword = generator.generateCrossword()
end = time.time()
# Print the time taken in minutes and seconds
print("Time taken: {} minutes and {} seconds".format(int((end-start)/60), int((end-start)%60)))
crossword.printGrid()
crossword.printBlankGrid()
print("Words added: {}".format(crossword.numWords))
print("Intersections: {}".format(crossword.numberOfIntersections))
crosswordPrinter(crossword, theme)