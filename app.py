# Import the crossword class from crossword_generator
from crossword_generator import CrosswordGenerator
# Import the config file
import config
# Import the prompts file
import prompts
# Import the openai library
import openai

# Get the openai key from config.py
openai.api_key = config.openAIKey

numClues = 20
theme = input("What is the theme of the crossword?\n")

# Test the openai call
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"system","content":prompts.roleOne},
        {"role":"user","content":str(numClues)},
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
#print(response.choices[0].message.content)

# Turn the response into a list
responseList = response.choices[0].message.content.splitlines()
for line in responseList:
    print(line)