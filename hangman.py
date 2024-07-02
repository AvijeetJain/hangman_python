import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display dimensions
winHeight = 480
winWidth = 700
win = pygame.display.set_mode((winWidth, winHeight))

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (102, 255, 255)

# Load fonts
btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)

# Initialize game variables
word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load(f'assets/hangman{i}.png') for i in range(7)]
limbs = 0

def redraw_game_window():
    """
    Function to redraw the game window, including buttons, guessed letters, and hangman image.
    """
    global guessed, hangmanPics, limbs

    win.fill(WHITE)

    # Draw buttons
    for btn in buttons:
        if btn[4]:
            pygame.draw.circle(win, BLACK, (btn[1], btn[2]), btn[3])
            pygame.draw.circle(win, btn[0], (btn[1], btn[2]), btn[3] - 2)
            label = btn_font.render(chr(btn[5]), 1, BLACK)
            win.blit(label, (btn[1] - (label.get_width() / 2), btn[2] - (label.get_height() / 2)))

    # Draw the guessed word with spaces
    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    win.blit(label1, (winWidth / 2 - length / 2, 400))

    # Draw hangman image
    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth / 2 - pic.get_width() / 2 + 20, 150))
    pygame.display.update()

def randomWord():
    """
    Function to select a random word from a file.
    """
    with open('words.txt') as file:
        words = file.readlines()
    return random.choice(words).strip()

def hang(guess):
    """
    Function to check if the guessed letter is in the word.
    """
    global word
    return guess.lower() not in word.lower()

def spacedOut(word, guessed=[]):
    """
    Function to display the word with guessed letters and underscores for remaining letters.
    """
    spacedWord = ''
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            if word[x].upper() in guessed:
                spacedWord = spacedWord[:-2] + word[x].upper() + ' '
        else:
            spacedWord += ' '
    return spacedWord

def buttonHit(x, y):
    """
    Function to check if a button was clicked based on mouse coordinates.
    """
    for btn in buttons:
        if x < btn[1] + 20 and x > btn[1] - 20 and y < btn[2] + 20 and y > btn[2] - 20:
            return btn[5]
    return None

def end(winner=False):
    """
    Function to handle the end of the game, displaying a win or loss message and resetting the game.
    """
    global limbs
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'

    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(WHITE)

    label = lost_font.render(winTxt if winner else lostTxt, 1, BLACK)
    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    win.blit(wordTxt, (winWidth / 2 - wordTxt.get_width() / 2, 295))
    win.blit(wordWas, (winWidth / 2 - wordWas.get_width() / 2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                reset()
                return

def reset():
    """
    Function to reset the game state.
    """
    global limbs, guessed, buttons, word

    for btn in buttons:
        btn[4] = True

    limbs = 0
    guessed = []
    word = randomWord()

# Setup buttons
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

# Select random word to start
word = randomWord()
inPlay = True

# Main game loop
while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

# Quit Pygame
pygame.quit()
