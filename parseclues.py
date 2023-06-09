import json

def parseClues(inputFromAPI):
    '''Takes the output from the API and returns a list of clues'''
    # Find the start of the data marked by [
    try:
        start = inputFromAPI.index('[')
    except ValueError:
        return print("Error: OpenAI returned an invalid response. The response was:", inputFromAPI)

        
    # Find the end of the data marked by ]
    end = inputFromAPI.index(']', start+1)
    # Get the data, including the brackets
    data = inputFromAPI[start:end+1]

    # Load the data as JSON
    processedData = json.loads(data)
    
    # Create a 2D array of the clues, word then clue
    clues = []
    for clue in processedData:
        clues.append([clue['word'], clue['clue']])

    return clues