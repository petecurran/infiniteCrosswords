import json

def parseClues(inputFromAPI):
    '''Takes the output from the API and returns a list of clues'''
    # Find the start of the data marked by [
    start = inputFromAPI.index('[')
    # Find the end of the data marked by ]
    end = inputFromAPI.index(']', start+1)
    # Get the data, including the brackets
    data = inputFromAPI[start:end+1]

    # Load the data as JSON
    processedData = json.loads(data)
    
    # Add each clue in the data to the clues list
    clues = []
    for clue in processedData:
        clues.append(clue)

    return clues