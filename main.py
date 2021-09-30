import pygame
import pygame_gui

from grid import Grid 
from colors import *
from button import Button
from save_load import save, load
from LogicComponents import ANDGate, Diode, NOTGate, OrGate
from LogicComponents import Generator, Line, Timer_comp, XORGate

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((700,670))
pygame.display.set_caption('')
FPS = 60
manager = pygame_gui.UIManager(
    (WIN.get_width(), WIN.get_height()), './themePygame_gui.json')


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', 
            fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


def createbuttons(board: Grid):

    row_items = ((WIN.get_width()-board.width)-10)//60
    row_gap = 15
    col_gap = (((WIN.get_width()-board.width)/row_items) - 60)/2
    start = board.width
    y = 110
    n = 1
    y_count = 0


    # creating buttons
    for name,func in [
        ('Clear', lambda : board.clear()),
        ('Save', lambda : save(board)),
        ('Start', lambda : board.start()),
        ('Load', lambda : load(board)),
        ('Red', lambda : board.toggle_red()),
    ]:
        Button(relative_rect=pygame.Rect((start+n*row_gap, y + y_count*col_gap), (60, 45)), text=name,
        manager=manager, tool_tip_text=None, func= func)

        # updating so the buttons will go next to each other
        start += 50
        n += 1
        # if the buttons fill the  whole width then they are pushed down
        if start+n*row_gap > WIN.get_width() - 60:
            start = board.width
            n = 1
            y_count += 1
            y += 60

    y = board.height + 15
    x = 40
    for name, func in [
        ('OR', lambda : board.set_component(OrGate)),
        ('Supply', lambda: board.set_component(Generator)),
        ('Line', lambda: board.set_component(Line)),
        ('Diode', lambda : board.set_component(Diode)),
        ('Timer', lambda : board.set_component(Timer_comp)),
        ('NOT', lambda : board.set_component(NOTGate)),
        ('XOR', lambda : board.set_component(XORGate)),
        ('AND', lambda : board.set_component(ANDGate))

    ]:
        Button(relative_rect=pygame.Rect((x, y), (60, 40)), text=name,
        manager=manager, tool_tip_text=None, func= func)
        x += 60 + 10
        # +n*row_gap

def checkKeypress(board):
    global boardClr
    if event.key == pygame.K_SPACE:
        board.start()

    if event.key == pygame.K_c:
        board.clear()

    if event.key == pygame.K_s:
        board.save()

    if event.key == pygame.K_o:
        board.load()

    if event.key == pygame.K_r:
        board.randomBoard()


board = Grid(75, 75, 600, 600, WIN)

createbuttons(board)

runGameOfLife = False
run = True
while run:

    clock.tick(FPS)
    time_delta = clock.tick(FPS)/1000.0

    # checks for left click
    if pygame.mouse.get_pressed()[0]:
        if board.runGameOfLife:
            board.start()
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        board.clicked(y, x)

    # checks for right click
    elif pygame.mouse.get_pressed()[2]:
        if board.runGameOfLife:
            board.start()
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        board.delete(y, x)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            checkKeypress(board)

        manager.process_events(event)

    WIN.fill(absBlack)

    board.update()

    manager.update(time_delta)
    manager.draw_ui(WIN)

    pygame.display.update()


pygame.quit()
