import os
from PIL import Image, ImageDraw, ImageFont

def crosswordPrinter (crossword, theme):
    '''Generates a HTML grid of the crossword provided for printing.'''

    # Generate HTML table rows for the height of the crossword
    tableString = ""
    for row in range(crossword.height):
        # Add a row to the table
        tableString += "<tr>"
        # Add a cell for each column
        for column in range(crossword.width):
            # Get the cell from the crossword
            cell = crossword.blankGrid[row][column]

            # If the cell is empty, use the empty class
            if cell == "":
                tableString += "<td class='crosswordcell bg-dark'></td>"

            # If the cell has a number, it's a clue. Use the clue class
            elif cell.isdigit():
                tableString += "<td class='crosswordcell cluenumber'>"+ cell +"</td>"

            # Otherwise, add a white cell to the table
            else:
                # Add the cell to the table
                tableString += "<td class='crosswordcell'></td>"

        # Close the row
        tableString += "</tr>"


    # Get the current directory
    currentDirectory = os.getcwd()

    # Get the path to the template file
    templatePath = os.path.join(currentDirectory, "infiniteCrosswords/template.html")

    # Open the template file
    with open(templatePath, "r") as template:
        # Read the file
        output = template.read()

    # Replace the theme with the theme provided
    output = output.replace("<!--Theme goes here-->", theme)

    # Replace the table with the table generated
    output = output.replace("<!--Table cells here-->", tableString)

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
    cell_size = 50
    img_width = cell_size * crossword.width
    img_height = cell_size * crossword.height
    img = Image.new('RGB', (img_width, img_height), color='white')
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
                # Draw a black cell
                draw.rectangle((cell_x, cell_y, cell_x + cell_size, cell_y + cell_size), fill='black')
            elif cell == '_':
                # Draw a white cell
                draw.rectangle((cell_x, cell_y, cell_x + cell_size, cell_y + cell_size), fill='white', outline='black')
            elif cell.isdigit():
                # Draw a white cell with the clue number
                draw.rectangle((cell_x, cell_y, cell_x + cell_size, cell_y + cell_size), fill='white', outline='black')
                draw.text((cell_x + 5, cell_y + 5), cell, fill='black', font=font)
                
    return img
