"""
Picaria Game w/ UDP Connection (Player 2)
- Raymond Zhang and Lev Shlyonsky

Emulates a game of Picaria, which is a two player
Indigenous American game from Southwestern USA.
Picaria is very similar to TicTacToe, which the
exception of only having three pieces each and
being able to move the pieces.

This python program features a GUI created using
pygame and uses a UDP connection to play with
another user. Additionally, it includes audio
cues as well as a menu and rule interface.

This is the player 2 version of the program. It
will always go second and is the white tile.
"""

import pygame
import socket
import sys

pygame.init()

# Connection variables
MY_IP = "" # IP of this device
RCV_IP = "" # IP of second player
UDP_PORT = 5005

# Colours
BLUE = "#77C3EC"
BLACK = "#262626"
BEIGE = "#f5f5dc"

# Sounds
invalidSound = pygame.mixer.Sound("assets/sounds/invalid.wav")
clickSound = pygame.mixer.Sound("assets/sounds/click.wav")
selectSound = pygame.mixer.Sound("assets/sounds/select.wav")

# Display settings
BOARD_SIZE = 600
BOARD_MARGIN = BOARD_SIZE // 6
OFFSET = 40
cell_size = BOARD_SIZE // 3
margin = 10
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))

# Font settings
SNIGLET = "assets/fonts/Sniglet-Regular.ttf"
H1_FONT = pygame.font.Font(SNIGLET, 60)
H2_FONT = pygame.font.Font(SNIGLET, 40)
P_FONT = pygame.font.Font(SNIGLET, 25)

# Game variables
P1 = 'O' # white
P2 = '@' # black
p1Chosen = True
p2Chosen = False
initialPos = None
moves = 0
currentPlayer = "black"
board = [['' for _ in range(3)] for _ in range(3)]

# Display functions

# Shortform for rendering text onto the display
def createText(text, font, colour=BLACK):
    return font.render(text, True, colour)

# Creates an interactive button with specificed dimensions and coordinates
def createButton(msg, x, y, w, h, initialColour, activeColour, clickPos, id=0, action=None):
    global hover
    mouse = pygame.mouse.get_pos() # position of mouse cursor

    # Cursor is on button
    if x+w > mouse[0] > x and y+h > mouse[1] > y:

        # Display active state
        pygame.draw.rect(screen, activeColour, (x,y,w,h), 0, 2)
        textSurf = createText(msg, P_FONT, BEIGE)

        # Ensures that hover sound will only play once when hovering
        if hover[id]:
            playSound(selectSound)
            hover[id] = False

        # Perform action once button is clicked
        if x+w > clickPos[0] > x and y+h > clickPos[1] > y and action != None:
            playSound(clickSound)
            action()

    else:
        hover[id] = True

        # Display inactive state
        pygame.draw.line(screen, initialColour,(x,y+h),(x+w,y+h), 2)
        textSurf = createText(msg, P_FONT, BLACK)

    screen.blit(textSurf, textSurf.get_rect(center=((x+(w/2)),(y+(h/2)))))

# Game's menu page
def displayMenu():
    global menu, hover

    # Set hover states for three buttons
    hover = [False]*3

    # Keep refreshing display
    menu = True
    while menu:
        clickPos = (0,0)
        # Get game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Get click position if iu xcuser clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = event.pos

        # Set display styles and text
        screen.fill(BEIGE)
        h1Text = createText("PICARIA", H1_FONT)
        screen.blit(h1Text, h1Text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 4)))

        # Display buttons
        createButton("play", BOARD_SIZE // 2 - 35, 240, 70, 35, BLACK, BLACK, clickPos, 0, gameLoop)
        createButton("rules", BOARD_SIZE // 2 - 35, 300, 70, 35, BLACK, BLACK, clickPos, 1,  displayRules)
        createButton("quit", BOARD_SIZE // 2 - 35, 360, 70, 35, BLACK, BLACK, clickPos, 2, displayQuit)

        # Update display
        pygame.display.update()
        pygame.time.Clock().tick(30)


# Show game information and rules
def displayRules():
    global counter, rules, showingRules

    counter = 0   # Keeps track of the current sentence/phrase
    rules = [
        "Welcome to Picaria!",
        "Picaria is variant of the popular TicTacToe and originates from Indigenous Southwestern USA (Muttiah).",
        "Picaria is played by two players (black and white), who will take turns placing their tiles onto the board.",
        "Similar to TicTacToe, players win by aligning three tiles in a row.",
        "However, each player can only place three tiles.",
        "After placing down all of their tiles, a player will only be able to move their tiles to adjacent spots on the grid.",
        "Adjacent spots are empty spots that are directly next to the selected tile, including diagonals.",
        "The best part about Picaria is that there are no possible ties; you must apply your logical thinking to find the winning move!",
        "Good Luck!"
    ]

    # Keep refreshing display
    showingRules = True
    while showingRules:
        clickPos = (0,0)
        # Get game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Get click position if user clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = event.pos

        # Set display styles and text
        screen.fill(BEIGE)
        wrapText(rules[counter], P_FONT, BLACK, BOARD_SIZE//2, BOARD_SIZE//5,400)

        # Display buttons
        createButton("next" if counter < len(rules)-1 else "menu", BOARD_SIZE // 2 - 35, 320, 70, 35, BLACK, BLACK, clickPos, 0, nextPage)

        # Update display
        pygame.display.update()
        pygame.time.Clock().tick(30)

# Show final quit screen
def displayQuit():
    global menu

    # Set display styles and text
    screen.fill(BEIGE)
    h1Text = createText("Thanks for playing!", H1_FONT)
    screen.blit(h1Text, h1Text.get_rect(center=(BOARD_SIZE // 2, 3*BOARD_SIZE // 8)))

    # Show screen for 750ms
    pygame.display.update()
    pygame.time.wait(750)

    # Exit out of menu loop
    menu = False

# Shortform for playing sound effects
def playSound(sound):
    pygame.mixer.Sound.play(sound)

# Iterates through the rules array
def nextPage():
    global counter, rules, showingRules

    # Increment counter
    counter += 1

    # Exit out of rule loop once counter is out of range
    showingRules = counter < len(rules)

# Wraps long strings of text into a nice box
def wrapText(text, font, colour, x, y, allowed_width):
    # Split the text into words
    words = text.split()

    # Construct lines out of words
    lines = []
    while len(words) > 0:
        # Get as many words as will fit within allowed_width
        line_words = []
        lineExceedsWidth = False
        while len(words) > 0 and not lineExceedsWidth:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                lineExceedsWidth = True

        # Add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    # Render each line below the last
    # Keep track of the cumulative height
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x - fw / 2
        ty = y + y_offset

        # Display line onto screen
        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh

# Game functions

# Displays the game board
def drawBoard():
    # Grid lines
    lines = [
            # Three horizontal lines
            (BOARD_MARGIN, BOARD_MARGIN, BOARD_SIZE-BOARD_MARGIN, BOARD_MARGIN), (BOARD_MARGIN, BOARD_SIZE//2, BOARD_SIZE-BOARD_MARGIN, BOARD_SIZE//2), (BOARD_MARGIN, BOARD_SIZE-BOARD_MARGIN, BOARD_SIZE-BOARD_MARGIN, BOARD_SIZE-BOARD_MARGIN),
            # Three vertical lines
            (BOARD_MARGIN, BOARD_MARGIN, BOARD_MARGIN, BOARD_SIZE-BOARD_MARGIN),(BOARD_SIZE//2, BOARD_MARGIN, BOARD_SIZE//2, BOARD_SIZE-BOARD_MARGIN), (BOARD_SIZE-BOARD_MARGIN, BOARD_SIZE-BOARD_MARGIN, BOARD_SIZE-BOARD_MARGIN, BOARD_MARGIN),
            # Two diagonals
            (BOARD_MARGIN, BOARD_MARGIN, BOARD_SIZE-BOARD_MARGIN, BOARD_SIZE-BOARD_MARGIN), (BOARD_MARGIN, BOARD_SIZE-BOARD_MARGIN, BOARD_SIZE-BOARD_MARGIN, BOARD_MARGIN),
            # Central diamond
            (BOARD_MARGIN, BOARD_SIZE//2, BOARD_SIZE//2, BOARD_MARGIN), (BOARD_MARGIN, BOARD_SIZE//2, BOARD_SIZE//2, BOARD_SIZE-BOARD_MARGIN), (BOARD_SIZE-BOARD_MARGIN, BOARD_SIZE//2, BOARD_SIZE//2, BOARD_MARGIN), (BOARD_SIZE-BOARD_MARGIN, BOARD_SIZE//2, BOARD_SIZE//2, BOARD_SIZE-BOARD_MARGIN)
        ]

    # Draw grid lines onto the display
    winner = checkWin()
    for i in range(len(lines)):
        line = lines[i]

        # Indicate winner by drawing a thicker line
        width = 10 if winner and winner[1] == i else 2

        pygame.draw.line(screen, BLACK, (line[0], line[1]+OFFSET), (line[2], line[3]+OFFSET), width)

    # Draw tiles onto the grid
    for row in range(3):
        for col in range(3):
            if board[row][col] == '@':
                drawTile(row, col, BLACK)
            elif board[row][col] == 'O':
                drawTile(row, col, "white")

# Draws the game tiles
def drawTile(row, col, color):
    # Calculate coordinates
    x_pos = col * cell_size + cell_size // 2
    y_pos = row * cell_size + cell_size // 2 + OFFSET

    pygame.draw.circle(screen, color, (x_pos, y_pos), cell_size // 5)

    # Draw borders
    pygame.draw.circle(screen, (BLUE if (row,col) == initialPos else BLACK), (x_pos, y_pos), cell_size // 5, 2)

# Check if a selected tile can be moved
def checkInitialClick(row, col):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for dr, dc in directions:
        newRow, newCol = row + dr, col + dc
        if 0 <= newRow < 3 and 0 <= newCol < 3 and board[newRow][newCol] == '' and board[row][col] == P1:
            return True
    return False

# Check if move location is valid
def validMove(row, col, newRow, newCol):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for dr, dc in directions:
        if newRow == row + dr and newCol == col + dc:
            if 0 <= newRow < 3 and 0 <= newCol < 3:
                if board[newRow][newCol] == '':
                    return True
    return False

# Check if game has been won
def checkWin():
    for i in range(3):
        # Win on a row
        if board[i][0] == board[i][1] == board[i][2] != '':
            return (board[i][0], i)

        # Win on a column
        if board[0][i] == board[1][i] == board[2][i] != '':
            return (board[0][i], i+3)

    # Win on the left diagonal
    if board[0][0] == board[1][1] == board[2][2] != '':
        return (board[0][0], 6)

    # Win on the right diagonal
    if board[0][2] == board[1][1] == board[2][0] != '':
        return (board[0][2], 7)

    # Game has not been won
    return None

# Adjusts board according to received move
def getMove():
    global board, P2

    # Get move information
    dataList = receiveMove()

    # Assume received data is a move operation
    try:
        row, col, newRow, newCol = dataList
        board[row][col] = ''
        board[newRow][newCol] = P2
    # Otherwise, place tile
    except:
        row, col = dataList
        board[row][col] = P2


# Connection Functions

# Get move from other user
def receiveMove():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((MY_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024)

    # Unpack move data from byte string into list
    dataList = list(map(int, data.decode().split('-')))
    return dataList

# Send move to other user
def sendMove(moveList):
    # Package player move information
    data = '-'.join(map(str, moveList))

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    # Send encoded data
    sock.sendto(data.encode(), (RCV_IP, UDP_PORT))

# Main game code
def gameLoop():
    global board, moves, currentPlayer, P1, initialPos, p1Chosen, p2Chosen

    # Keep refreshing display
    running = True
    while running:
        # Get game events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Once user clicks somewhere on the screen
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Play game as usual
                if not winner:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    col = mouse_x // cell_size
                    row = mouse_y // cell_size

                    # Players are still placing tiles
                    if moves < 6 and currentPlayer == "white":
                        # Place tile and send move if player 2
                        if not p1Chosen:
                            if board[row][col] == '' and not checkWin():
                                board[row][col] = P1
                                p1Chosen = True
                                p2Chosen = False
                                sendMove([row, col])
                                drawBoard()

                                # Update game states
                                currentPlayer = "white" if currentPlayer == "black" else "black"
                                moves += 1
                                playSound(clickSound)

                        #! DEBUG (remove)
                        print("Player " + currentPlayer + "'s turn")

                    # Game is in move phase
                    elif moves >= 6 and currentPlayer == "white":
                        # Select tile to move
                        if initialPos is None:
                            # Check if selected tile is valid
                            if checkInitialClick(row, col):

                                # Get selected tile
                                initialPos = (row, col)
                                playSound(selectSound)

                                # ! DEBUG (remove)
                                print("Choose position: ", initialPos)

                            else:

                                playSound(invalidSound)

                                # ! DEBUG (remove)
                                print("Not available. Try again.")

                        # Select move location
                        else:
                            # Check if move location is valid
                            if validMove(initialPos[0], initialPos[1], row, col) and board[row][col] == '' and not p1Chosen:

                                # Place tile and send move if player 2
                                if currentPlayer == "white":
                                    board[row][col] = P1
                                    board[initialPos[0]][initialPos[1]] = ''
                                    sendMove([initialPos[0], initialPos[1], row, col])

                                    # Update flags
                                    p1Chosen = True
                                    p2Chosen = False

                                    # Update game states
                                    initialPos = None
                                    currentPlayer = "white" if currentPlayer == "black" else "black"
                                    moves += 1
                                    playSound(clickSound)

                                # ! DEBUG
                                print("Move successful!")
                                print("Player " + currentPlayer + "'s turn")

                            else:
                                playSound(invalidSound)

                                # Reset selected tile
                                initialPos = None

                                # ! DEBUG (remove)
                                print("Invalid move. Try again.")

                # Exit game on click once game is over
                else:
                    running = False

        # Render game styles, board, and text

        screen.fill(BEIGE)
        drawBoard()

        # Adjust game text according to game state
        p_text = f"{'placing' if moves < 6 else 'moving'}: {currentPlayer}"
        winner = checkWin()
        if winner:
            p_text = f"{'white' if winner[0] == 'O' else 'black'} wins!"

        h1Text = createText("PICARIA", H2_FONT)
        screen.blit(h1Text, (100,25))
        p1Text = createText(p_text, P_FONT)
        p1Rect = p1Text.get_rect()
        setattr(p1Rect, "topright", (500,40))
        screen.blit(p1Text, p1Rect)

        # Update display
        pygame.display.update()
        pygame.time.Clock().tick(30)

        # Get move from player 1
        if currentPlayer == "black" and not p2Chosen and winner is None:
            # Reset flags
            p1Chosen = False
            p2Chosen = True

            # Update game settings
            currentPlayer = "white" if currentPlayer == "black" else "black"
            moves += 1

            getMove()

    # Reset game variables once game is done
    p1Chosen = True
    p2Chosen = False
    initialPos = None
    moves = 0
    currentPlayer = "black"
    board = [['' for _ in range(3)] for _ in range(3)]

# Driver code
def main():
    pygame.display.set_caption("Picaria")
    gameIcon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(gameIcon)
    displayMenu()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()