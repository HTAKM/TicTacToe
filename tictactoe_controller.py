import pygame
from pygame.locals import *
from tictactoe_class import *
from time import sleep

bgcolor = (255,255,255)
textcolor = (0,0,0)
is_dark_mode = False
GAME = TicTacToe()
CAPTION = "Tic-Tac-Toe"
LEFT_BUTTON = 1
RIGHT_BUTTON = 3
CANVAS_SIZE = (500,600)
GAME_COOR = [100,200]
START_MENU_SCREEN = 0
GAME_SCREEN = 1
LINE_WIDTH = 3

pygame.init()
canvas = pygame.display.set_mode(CANVAS_SIZE)
pygame.display.set_caption(CAPTION)

TITLE_FONT = pygame.font.Font('freesansbold.ttf',32)
NORMAL_FONT = pygame.font.Font('freesansbold.ttf',16)

class Circle(pygame.sprite.Sprite):
    def __init__(self):
        super(Circle, self).__init__()
        self.surf = pygame.Surface((95,95))
        self.surf.fill(bgcolor)
        pygame.draw.circle(self.surf, (0,0,255), [47,47], 45, 5)
        self.rect = self.surf.get_rect()

class Cross(pygame.sprite.Sprite):
    def __init__(self):
        super(Cross, self).__init__()
        self.surf = pygame.Surface((95,95))
        self.surf.fill(bgcolor)
        pygame.draw.line(self.surf, (255,0,0), [5,5], [89,89], 5)
        pygame.draw.line(self.surf, (255,0,0), [5,89], [89,5], 5)
        self.rect = self.surf.get_rect()

class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, text = ""):
        super(Button, self).__init__()
        self.surf = pygame.Surface((width, height), depth = 32)
        self.surf.fill(bgcolor)
        self.rect = self.surf.get_rect()
        pygame.draw.rect(self.surf, textcolor, self.rect, 2)
        self.textfield = NORMAL_FONT.render(text, True, textcolor)

    def button_clicked(self, click_pos) -> bool:
        """
        Determine whether the button is clicked.
        """

        return self.rect.left <= click_pos[0] <= self.rect.right and self.rect.top <= click_pos[1] <= self.rect.bottom
    
    def show_text(self):
        """
        Show the text when the button is placed.
        """

        text = self.textfield.get_rect()
        text.center = self.rect.center
        canvas.blit(self.textfield, text)

def start_window():
    """
    Handle GUI for start menu screen.
    """

    global gameOn
    global play_button, dark_mode_button
    global screen

    clear_screen()
    gameOn = False
    text = TITLE_FONT.render('Tic-Tac-Toe', True, textcolor)
    textRect = text.get_rect()
    textRect.center = (CANVAS_SIZE[0] // 2, CANVAS_SIZE[1] // 2 - 100)
    play_button = Button(100,50, "Play")
    play_button.rect.center = (CANVAS_SIZE[0] // 2, CANVAS_SIZE[1] // 2 + 100)
    dark_mode_button = Button(50,50, "Light" if is_dark_mode else "Dark")
    dark_mode_button.rect.topright = (490, 10)
    canvas.blit(text, textRect)
    canvas.blit(play_button.surf, play_button.rect)
    canvas.blit(dark_mode_button.surf, dark_mode_button.rect)
    play_button.show_text()
    dark_mode_button.show_text()
    screen = START_MENU_SCREEN

def game_window():
    """
    Handle GUI for game screen.
    """

    global gameOn
    global squares
    global screen

    clear_screen()
    gameOn = True
    squares = [None for i in range(9)]
    pygame.draw.line(canvas, textcolor, [GAME_COOR[0]+100,GAME_COOR[1]], [GAME_COOR[0]+100,GAME_COOR[1]+300], 5)
    pygame.draw.line(canvas, textcolor, [GAME_COOR[0]+200,GAME_COOR[1]], [GAME_COOR[0]+200,GAME_COOR[1]+300], 5)
    pygame.draw.line(canvas, textcolor, [GAME_COOR[0],GAME_COOR[1]+100], [GAME_COOR[0]+300,GAME_COOR[1]+100], 5)
    pygame.draw.line(canvas, textcolor, [GAME_COOR[0],GAME_COOR[1]+200], [GAME_COOR[0]+300,GAME_COOR[1]+200], 5)
    restart_text = NORMAL_FONT.render('Press R to reset', True, textcolor)
    restart_textRect = restart_text.get_rect()
    restart_textRect.center = (CANVAS_SIZE[0] // 2, 150)
    canvas.blit(restart_text, restart_textRect)
    turn_visual()
    screen = GAME_SCREEN

def start_screen_process(event):
    """
    Handle events when start menu screen is visualized.
    """

    if event.type == MOUSEBUTTONDOWN:
        if event.button == LEFT_BUTTON:
            if play_button.button_clicked(event.pos):
                clear_screen()
                game_window()
            elif dark_mode_button.button_clicked(event.pos):
                dark_mode()

def dark_mode():
    """
    Switch between dark mode and light mode. This should only be used in start menu screen.
    """

    global bgcolor, textcolor
    global is_dark_mode
    global dark_mode_button

    bgcolor, textcolor = textcolor, bgcolor
    is_dark_mode = not is_dark_mode
    start_window()

def game_screen_process(event):
    """
    Handle events when game screen is visualized.
    """

    if event.type == KEYDOWN:
        if event.key == K_r:
            restart_game_state()
    elif gameOn and event.type == MOUSEBUTTONDOWN and event.button == LEFT_BUTTON:
        pos = obtain_click_pos(GAME_COOR, event.pos)
        if pos == -1: return
        if not GAME.game_state[pos]:
            squares[pos] = Cross() if GAME.is_x_turn() else Circle()
            GAME.player_move(pos)
            visualize_game_state(pos)
            win = GAME.is_winner()
            if any(state == 0 for state in GAME.game_state) and not win:
                GAME.next_turn()
                turn_visual()
            else:
                end_state(win)

def event_process(screen):
    """
    Different screen has different event behaviour.
    """

    if screen == START_MENU_SCREEN: return lambda e: start_screen_process(e)
    elif screen == GAME_SCREEN: return lambda e: game_screen_process(e)

def turn_visual():
    """
    Change the game text after every turn.
    """

    global game_text
    canvas.fill(bgcolor, pygame.Rect(0,0,CANVAS_SIZE[0],120))
    game_text = NORMAL_FONT.render(f'{GAME.print_player()}\'s turn', True, textcolor)
    game_textRect = game_text.get_rect()
    game_textRect.center = (CANVAS_SIZE[0] // 2, 100)
    canvas.blit(game_text, game_textRect)

def clear_screen(): 
    """
    Clear the entire screen by filling it with background colours.
    """

    canvas.fill(bgcolor)

def visualize_game_state(pos):
    squares[pos].rect.left = GAME_COOR[0] + (pos % 3) * 100 + LINE_WIDTH
    squares[pos].rect.top = GAME_COOR[1] + (pos // 3) * 100 + LINE_WIDTH
    canvas.blit(squares[pos].surf, squares[pos].rect)

def restart_game_state():
    """
    Clear out the tic-tac-toe grid and start the game.
    """

    global gameOn
    GAME.initialize_game_state()
    turn_visual()
    for square in squares:
        if not square == None:
            canvas.fill(bgcolor, square.rect)
    gameOn = True

def end_state(player_won):
    """
    Perform last display change after game ends when a player wins or it is a draw.
    """

    global gameOn
    global game_text
    canvas.fill(bgcolor, pygame.Rect(0,0,CANVAS_SIZE[0],120))
    if player_won:
        game_text = NORMAL_FONT.render(f'{GAME.print_player()} wins', True, textcolor)
    else:
        game_text = NORMAL_FONT.render(f'It is a draw!', True, textcolor)
    game_textRect = game_text.get_rect()
    game_textRect.center = (CANVAS_SIZE[0] // 2, 100)
    canvas.blit(game_text, game_textRect)
    gameOn = False

if __name__ == '__main__':
    exit = False
    start_window()
    while not exit:
        for event in pygame.event.get():
            if event.type == QUIT or \
               (event.type == KEYDOWN and event.key == K_ESCAPE):
                exit = True
                continue
            event_process(screen)(event)
        pygame.display.flip()
