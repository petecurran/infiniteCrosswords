from parseclues import parseClues
from crossword_generator import CrosswordGenerator
from print_generator import crosswordPrinter, generateImage
import config
import prompts
import openai

# Get the openai key from config.py
# This is a file that is not included in the repository. It only requires one line:
# openAIKey = 'YOUROPENAIKEY'
openai.api_key = config.openAIKey

numAttempts = 20 # Number of attempts to generate a crossword. Higher is better but slower. Go and grab a coffee.
numClues = 20 # Number of clues to include. 20-40 works well. More theoretically possible but the crossword will be very small.
theme = input("What is the theme of the crossword?\n")

# Test the openai call
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"system","content":prompts.roleOne},
        {"role":"user","content":"Please supply {} clues.".format(str(numClues))},
        {"role":"user","content":"The topic for this crossword is '{}'.".format(theme)}
    ])

content = response.choices[0].message.content # Get the relevant bit from GPT's structured response
clues = parseClues(content) # Get the clues from the response.

generator = CrosswordGenerator(clues, 20) # Create a crossword generator with the clues and the number of attempts
crossword = generator.generateCrossword() # Generate the crossword
print("Words added: {}".format(crossword.numWords))
print("Intersections: {}".format(crossword.numberOfIntersections))

crosswordPrinter(crossword, theme) # Send the crossword to HTML files for printing.
print("Crossword saved to infiniteCrosswords/created_crosswords/")
input("Press enter to exit.")
