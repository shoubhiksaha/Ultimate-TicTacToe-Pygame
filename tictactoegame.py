# importing the required libraries
import pygame as pg
import sys
import time
from pygame.locals import *
import random  # Make sure this is imported at the top
# declaring the global variables

# for storing the 'x' or 'o'
# value as character
XO = 'x'
x1 = 'o'
ai_difficulty = "hard"
ai_level = "easy"  # can be "easy" or "hard"

is_player_turn = True  # X is usually player


# storing the winner's value at
# any instant of code
winner = None

# to check if the game is a draw
draw = False

# to set width of the game window
width = 400

# to set height of the game window
height = 400

# to set background color of the
# game window
white = (255, 255, 255)

# color of the straightlines on that
# white game board, dividing board
# into 9 parts
line_color = (0, 0, 0)

# setting up a 3 * 3 board in canvas
board = [[None]*3, [None]*3, [None]*3]


# initializing the pygame window
pg.init()

BIG_FONT = pg.font.Font(None, 60)  # Default system font, size 60

# setting fps manually
fps = 30

# this is used to track time
CLOCK = pg.time.Clock()

# this method is used to build the
# infrastructure of the display
screen = pg.display.set_mode((width, height + 120), 0, 32)

# setting up a nametag for the
# game window
pg.display.set_caption("My Tic Tac Toe")

font = pg.font.Font(None, 32)  

# loading the images as python object
initiating_window = pg.image.load("modified_cover.png")
x_img = pg.image.load("X_modified.png")
O_img = pg.image.load("o_modified.png")

# resizing images
initiating_window = pg.transform.scale(
    initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(O_img, (80, 80))
# Scoreboard variables
score_X = 0
score_O = 0
score_draw = 0

# Button colors
button_bg = (180, 180, 180)
button_active_bg = (100, 180, 100)
button_text_color = (0, 0, 0)

 # Game mode state
game_mode = "PvAI"  # default mode on startup


# Button rectangles
easy_button_rect = pg.Rect(30, height + 10, 100, 30)
hard_button_rect = pg.Rect(150, height + 10, 100, 30)
# Button rectangles (make global)
easy_button_rect = pg.Rect(30, height + 10, 100, 30)
hard_button_rect = pg.Rect(270, height + 10, 100, 30)
# Game mode buttons
pvp_button_rect = pg.Rect(270, height + 50, 100, 30)
pvai_button_rect = pg.Rect(30, height + 50, 100, 30)

pvp_text = font.render("PvP", True, white)
pvai_text = font.render("PvAI", True, white)

reset_rect = pg.Rect(width // 2 - 50, height + 55, 100, 30)
WIDTH = 600
HEIGHT = 600
SQUARE_SIZE = WIDTH // 3


def game_initiating_window():

    # displaying over the screen
    screen.blit(initiating_window, (0, 0))

    # updating the display
    pg.display.update()
    time.sleep(0.5)
   
    screen.fill(white)

    # drawing vertical lines
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0),
                 (width / 3 * 2, height), 7)

    #drawing horizontal lines
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2),
                 (width, height / 3 * 2), 7)
    draw_status()
    pg.display.update()


def draw_status():
    global draw, width, height, ai_difficulty

    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = "Game Draw!"

    font = pg.font.Font(None, 30)
    text = font.render(message, True, white)

    # Clear status area
    screen.fill((0, 0, 0), (0, height, width, 120))

    # Draw status message
    text_rect = text.get_rect(center=(width // 2, height + 25))
    screen.blit(text, text_rect)

    # Reset Button
    button_font = pg.font.Font(None, 28)
    button_text = button_font.render("Reset", True, (0, 0, 0))
    pg.draw.rect(screen, (200, 200, 200), reset_rect)
    screen.blit(button_text, button_text.get_rect(center=reset_rect.center))

    # Draw Scoreboard
    scoreboard_font = pg.font.Font(None, 24)
    score_text = f"X Wins: {score_X}    O Wins: {score_O}    Draws: {score_draw}"
    score_render = scoreboard_font.render(score_text, True, white)
    score_rect = score_render.get_rect(center=(width // 2, height + 110))
    screen.blit(score_render, score_rect)

    # --- AI Difficulty Buttons ---
    button_font = pg.font.Font(None, 24)
    pg.draw.rect(screen, button_active_bg if ai_difficulty == "easy" else button_bg, easy_button_rect)
    pg.draw.rect(screen, button_active_bg if ai_difficulty == "hard" else button_bg, hard_button_rect)

    easy_text = button_font.render("Easy AI", True, button_text_color)
    hard_text = button_font.render("Hard AI", True, button_text_color)

    screen.blit(easy_text, easy_text.get_rect(center=easy_button_rect.center))
    screen.blit(hard_text, hard_text.get_rect(center=hard_button_rect.center))
       
    # Game Mode Buttons
    pg.draw.rect(screen, button_active_bg  if game_mode == "PvP" else button_bg, pvp_button_rect)
    pg.draw.rect(screen, button_active_bg  if game_mode == "PvAI" else button_bg, pvai_button_rect)

    screen.blit(pvp_text, pvp_text.get_rect(center=pvp_button_rect.center))
    screen.blit(pvai_text, pvai_text.get_rect(center=pvai_button_rect.center))

   
    pg.display.update()

# Add this function after the draw_status() function and before user_click()
def drawXO(row, col):
    global board, XO

    x_pos = (col - 1) * width / 3 + 30
    y_pos = (row - 1) * height / 3 + 30

    if XO == 'x':
        screen.blit(x_img, (x_pos, y_pos))
        board[row - 1][col - 1] = 'x'
        XO = 'o'
    else:
        screen.blit(o_img, (x_pos, y_pos))
        board[row - 1][col - 1] = 'o'
        XO = 'x'

    pg.display.update()



def check_win():
    global board, winner, draw, score_X, score_O, score_draw

    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0), (0, (row + 1) * height / 3 - height / 6),
                         (width, (row + 1) * height / 3 - height / 6), 4)
            break

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0),
                         ((col + 1) * width / 3 - width / 6, height), 4)
            break

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    # Check draw
    if all([all(row) for row in board]) and winner is None:
        draw = True

    # Update scoreboard
    if winner == 'x':
        score_X += 1
    elif winner == 'o':
        score_O += 1
    elif draw:
        score_draw += 1

    draw_status()
    
def get_empty_cells():
    empty = []
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                empty.append((row, col))
    return empty


def check_draw():
    for row in board:
        for cell in row:
            if cell == '':
                return False
    return True if not winner else False

def user_click():
    global XO, winner, draw
 
    x, y = pg.mouse.get_pos()
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    if row < 3 and col < 3:
        if board[row][col] == '':
            board[row][col] = XO
            winner = check_win()
            draw = check_draw()
            if not winner and not draw:
                XO = 'x' if XO == 'o' else 'o'


    # get column
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    # get row
    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col and board[row-1][col-1] is None:
        XO
        
        drawXO(row, col)
        check_win()

        # Let AI play only in PvAI mode
        if game_mode == "PvAI" and not winner and not draw:
            XO = 'o'
            ai_move()
            XO = 'x'
        
        elif game_mode == "PvAI":
            if not winner and not draw:
                XO = 'o'
                ai_move()
                XO = 'x'

def ai_move():
    global XO
    if XO == 'o':
     if ai_difficulty == "easy":
        easy_ai_move()
     elif ai_difficulty == "hard":
        i, j = best_move()
        drawXO(i + 1, j + 1)
        check_win()

def is_winning_move(temp_board, player):
    # Check rows
    for row in range(3):
        if temp_board[row][0] == temp_board[row][1] == temp_board[row][2] == player:
            return True

    # Check columns
    for col in range(3):
        if temp_board[0][col] == temp_board[1][col] == temp_board[2][col] == player:
            return True

    # Check diagonals
    if temp_board[0][0] == temp_board[1][1] == temp_board[2][2] == player:
        return True

    if temp_board[0][2] == temp_board[1][1] == temp_board[2][0] == player:
        return True

    return False

def can_win(player):
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = player
                if is_winning_move(board, player):  # ✅ Use AI-compatible checker
                    board[row][col] = None
                    return (row, col)
                board[row][col] = None
    return None

def best_move():
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = 'o'
                score = minimax(board, 0, False)
                board[i][j] = None
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move
def check_terminal(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    # No winner
    return None

def minimax(board, depth, is_maximizing):
    global winner
    # Check terminal states
    if check_terminal(board) == 'o':
        return 1
    elif check_terminal(board) == 'x':
        return -1
    elif all([all(row) for row in board]):
        return 0

    if is_maximizing:
        best = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'o'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = None
                    best = max(score, best)
        return best
    else:
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'x'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = None
                    best = min(score, best)
        return best

import random  # Make sure this is imported at the top
def easy_ai_move():
    empty = get_empty_cells()
    if empty:
        row, col = random.choice(empty)
        drawXO(row + 1, col + 1)
        check_win()



def draw_result(text):
    result_text = BIG_FONT.render(text, True)
    text_rect = result_text.get_rect(center=(width // 2, height // 2))
    screen.blit(result_text, text_rect)
def check_victory(char):
    for row in board:
        if row.count(char) == 3:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == char:
            return True
    if board[0][0] == board[1][1] == board[2][2] == char:
        return True
    if board[0][2] == board[1][1] == board[2][0] == char:
        return True
    return False

def reset_button():
    global reset_rect
    reset_rect = pg.Rect(100,40,120,60)
    pg.draw.rect(screen,  reset_rect)
    reset_text = font.render("Reset", True, white)
    screen.blit(reset_text, (reset_rect.x + 10, reset_rect.y + 5))

def reset_game():
    global board, winner, XO, draw,is_player_turn
    
    time.sleep(1)

    XO = 'x'
    draw = False
    winner = None
    board = [[None]*3, [None]*3, [None]*3]
    screen.fill(white)
    game_initiating_window()
    
game_initiating_window()

# Main game loop
while True:
    
    pg.display.update()
    draw_status()
    pg.display.update()

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            # Check buttons
            if easy_button_rect.collidepoint(mouse_pos):
                ai_difficulty = "easy"
                draw_status()
                print("Switched to Easy AI")

            elif hard_button_rect.collidepoint(mouse_pos):
                ai_difficulty = "hard"
                draw_status()
                print("Switched to Hard AI")

            elif pvp_button_rect.collidepoint(mouse_pos):
                game_mode = "PvP"
                reset_game()
                print("Switched to PvP")

            elif pvai_button_rect.collidepoint(mouse_pos):
                game_mode = "PvAI"
                reset_game()
                print("Switched to PvAI")

            elif reset_rect.collidepoint(mouse_pos):
                reset_game()

            # Player click on game board
            elif mouse_pos[1] < height:
                if game_mode == "PvP":
                    user_click()
                elif game_mode == "PvAI" and XO == 'x' and not winner and not draw:
                    user_click()
                    # Let AI move next frame, not in this click event

    # Call AI move once per frame if it's AI's turn
    if game_mode == "PvAI" and XO == 'o' and not winner and not draw:
        pg.time.wait(100)  # Optional small delay
        ai_move()
        check_win()

