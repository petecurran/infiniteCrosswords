import os

def crosswordPrinter (crossword, theme):
    '''Generates a HTML grid of the crossword provided for printing.'''

    # Open the template file
    with open("template.html", "r") as template:
        # Read the file
        output = template.read()

    # Replace the theme with the theme provided
    output = output.replace("<!--Theme goes here-->", theme)

