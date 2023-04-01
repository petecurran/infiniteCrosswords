import os
from PIL import Image, ImageDraw, ImageFont

def crosswordPrinter (crossword, theme):
    '''Generates a HTML page of the crossword provided for printing.'''

    # Get the current directory
    currentDirectory = os.getcwd()

    # Get the path to the template file
    templatePath = os.path.join(currentDirectory, "infiniteCrosswords/template.html")

    # Get the path to the created_crosswords folder
    createdCrosswordsPath = os.path.join(currentDirectory, "infiniteCrosswords/created_crosswords")

    # Generate the image of the crossword
    img = generateImage(crossword)

    # Save the image to the img folder in created_crosswords
    imgPath = os.path.join(createdCrosswordsPath, "img")

    # Check if a file with this theme already exists
    if os.path.exists(os.path.join(imgPath, theme + ".png")):
        # If it does, add a number to the end of the file name
        i = 1

        # Loop until a file with the name doesn't exist
        while os.path.exists(os.path.join(imgPath, theme + str(i) + ".png")):
            i += 1

        # Save the image with the new name
        img.save(os.path.join(imgPath, theme + str(i) + ".png"))
        fileName = theme + str(i) + ".png"

    else:
        # Save the image with the theme as the name
        img.save(os.path.join(imgPath, theme + ".png"))
        fileName = theme + ".png"

    # Set the image path to the path of the image
    imagePath = "img/{}".format(fileName)

    # Set the image tag to the image path
    imageTag = "<img src=\"{}\" alt=\"{}\" id=\"crossword-image\">".format(imagePath, theme)
    
    #Update the title
    titleTag = "<title>Infinite Crosswords - {}</title>".format(theme)

    # Add a list element for each horizontal clue
    horizontalClues = ""
    for clue in crossword.horizontalClues:
        horizontalClues += "<li>{}. {} {}</li>".format(clue[0], clue[1], clue[2])

    # Add a list element for each vertical clue
    verticalClues = ""
    for clue in crossword.verticalClues:
        verticalClues += "<li>{}. {} {}</li>".format(clue[0], clue[1], clue[2])

    # Open the template file
    with open(templatePath, "r") as template:
        # Read the file
        output = template.read()

    # Replace the title with the theme provided
    output = output.replace("<!--Title goes here-->", titleTag)

    # Replace the theme with the theme provided
    output = output.replace("<!--Theme goes here-->", theme)

    # Replace the image tag with the image tag
    output = output.replace("<!--Image goes here-->", imageTag)

    # Replace the horizontal clues with the horizontal clues
    output = output.replace("<!--Horizontal clues go here-->", horizontalClues)

    # Replace the vertical clues with the vertical clues
    output = output.replace("<!--Vertical clues go here-->", verticalClues)

    # Set the output directory to the created_crosswords folder
    outputDirectory = os.path.join(currentDirectory, "infiniteCrosswords/created_crosswords")

    # Create the file name in the directory
    fileName = os.path.join(outputDirectory, theme + ".html")

    # Open the output file
    with open(fileName, "w") as outputHTML:
        # Write the output to the file
        outputHTML.write(output)

    # Open the output file in the default browser
    os.startfile(fileName)

    return

def generateImage(crossword):
    # Set up the image and drawing context
    cell_size = 25
    img_width = cell_size * crossword.width
    img_height = cell_size * crossword.height
    img = Image.new('RGBA', (img_width+1, img_height+1), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    # Set up the font for the clue numbers
    font_size = int(cell_size * 0.4)
    font = ImageFont.truetype('arial.ttf', font_size)
    
    # Draw the grid
    for y, row in enumerate(crossword.blankGrid):
        for x, cell in enumerate(row):
            # Calculate the coordinates of the cell
            cell_x = x * cell_size
            cell_y = y * cell_size
            
            if cell == '':
                # Draw a blank cell with no outline
                draw.rectangle((cell_x, cell_y, cell_x + cell_size, cell_y + cell_size), outline='black', width=0)
                
            elif cell == '_':
                # Draw a white cell
                draw.rectangle((cell_x, cell_y, cell_x + cell_size, cell_y + cell_size), fill='white', outline='black', width=1)
            elif cell.isdigit():
                # Draw a white cell with the clue number
                draw.rectangle((cell_x, cell_y, cell_x + cell_size, cell_y + cell_size), fill='white', outline='black', width=1)
                draw.text((cell_x + 5, cell_y + 5), cell, fill='black', font=font)
                
    return img
