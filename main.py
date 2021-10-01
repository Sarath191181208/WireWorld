import pygame
from pygame.locals import MOUSEWHEEL
import pygame_gui
import os
from threading import Thread

from components.grid import Grid  
from components.colors import *
from components.button import Button
from components.save_load import save, load
from components.LogicComponents import ANDGate, Diode, NOTGate, OrGate
from components.LogicComponents import Generator, Line, Timer_comp, XORGate

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((590,570))
pygame.display.set_caption('')
FPS = 60
manager = pygame_gui.UIManager(
    (WIN.get_width(), WIN.get_height()), os.path.join('themes','./themePygame_gui.json'))


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', 
            fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


def createbuttons(board: Grid):

    row_items = ((WIN.get_width()-board.width)-10)//60
    row_gap = 15
    col_gap = (((WIN.get_width()-board.width)/row_items) - 60)/2
    start = board.width
    y = 60
    n = 1
    y_count = 0


    # creating buttons
    for name,func in [
        ('Clear', lambda : board.clear()),
        ('Save', lambda : save(board)),
        ('Start', lambda : board.start()),
        ('Load', lambda : load(board)),
        ('Red', lambda : board.toggle_red()),
        ('Pan', lambda : board.toggle_pan())
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
    x = 10
    for name, func in [
        ('Supply', lambda: board.set_component(Generator)),
        ('Line', lambda: board.set_component(Line)),
        ('Timer', lambda : board.set_component(Timer_comp)),
        ('Diode', lambda : board.set_component(Diode)),
        ('OR', lambda : board.set_component(OrGate)),
        ('NOT', lambda : board.set_component(NOTGate)),
        ('XOR', lambda : board.set_component(XORGate)),
        ('AND', lambda : board.set_component(ANDGate))
    ]:
        Button(relative_rect=pygame.Rect((x, y), (60, 40)), text=name,
        manager=manager, tool_tip_text=None, func= func)
        x += 60 + 12
        # +n*row_gap

def checkKeypress(board: Grid):

    if event.key == pygame.K_SPACE:
        board.start()

    if event.key == pygame.K_c:
        board.clear()

    if event.key == pygame.K_s:
        save(board)

    if event.key == pygame.K_o:
        load(board)

    if event.key == pygame.K_r:
        board.toggle_red()
    
    if event.key == pygame.K_p:
        board.toggle_pan()



board = Grid(100, 100, 500, 500, WIN)

createbuttons(board)

runGameOfLife = False
run = True
while run:

    clock.tick(FPS)
    time_delta = clock.tick(FPS)/1000.0

    # checks for left click
    if board.pan_selected:
            board.pan() 
    elif pygame.mouse.get_pressed()[0]:
        if board.runGameOfLife:
                board.start()
        board.clicked()

    # checks for right click
    elif pygame.mouse.get_pressed()[2]:
        if board.runGameOfLife:
            board.start()
        board.delete()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            checkKeypress(board)
        
        if event.type == MOUSEWHEEL:
            board.set_scale( event.y * -0.25)

        manager.process_events(event)

    WIN.fill(absBlack)
    thread = Thread(target= board.update(), args=(10,))
    thread.start()

    manager.update(time_delta)
    manager.draw_ui(WIN)
    thread.join()


    pygame.display.update()


pygame.quit()
