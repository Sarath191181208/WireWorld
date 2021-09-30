import pygame 
from colors import *
import random
from timer import Timer 

class Grid():
    def __init__(self, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400, WIN=None):
        self.rows = cols
        self.cols = rows
        self.WIN = WIN
        self.cubes = [
            [Cube(0, i, j, width, height, self.cols, self.rows, self.WIN)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.width = width
        self.height = height

        self.runGameOfLife = False
        self.conway_timer = Timer(0.1, func=lambda:self.Conway(), loop=True)

        self.start_btn_timer = Timer(0.2)
        self.click_timer = Timer(0.15)

        self.draw_component = False
        self.component = None

        self.draw()

    def randomBoard(self):
        for x in range(self.rows):
            for y in range(self.cols):
                self.cubes[x][y].delete()
                self.cubes[x][y].value = random.randint(0, 1)
                self.cubes[x][y].draw()
        self.draw()

    def draw(self, win=None):
        win = self.WIN

        background = pygame.Surface((self.width,self.height))
        win.blit(background,(0,0))

        rowGap = self.height / self.rows
        colGap = self.width / self.cols

        thick = 1

                # Draw Cubes
        for row in self.cubes:
            for cube in row:
                cube.draw()

        for i in range(self.rows+1):
            pygame.draw.line(win, BLACK, (0, i*rowGap),(self.height, rowGap*i), thick)

        for j in range(self.cols+1):
            pygame.draw.line(win, BLACK, (j*colGap, 0), (colGap*j, self.width),thick)

    def Conway(self):
        for row in self.cubes:
            for cube in row:
                cube.iter(self.cubes)

        for row in self.cubes:
            for cube in row:
                cube.set_next()

    def start(self):
        if not self.start_btn_timer.start:
            self.runGameOfLife = not self.runGameOfLife
            self.conway_timer.stop_timer()
            self.start_btn_timer.start_timer()

    def clear(self):
        for row in self.cubes:
            for cube in row:
                cube.reset()
        self.runGameOfLife = False
        self.draw()

    def clicked(self, i, j):
        if self.click_timer.start:
            return
        if self.runGameOfLife:
            return
        if i < 0 or j < 0 or i >= self.rows or j >= self.cols:
            return -1

        if self.draw_component:

            self.apply_component(self.component, i, j)
            return

        self.click_timer.start_timer()
        self.cubes[i][j].clicked()

    def delete(self, x, y):
        if self.click_timer.start:
            return
        if self.runGameOfLife:
            return
        if x < 0 or y < 0 or x >= self.rows or y >= self.cols:
            return -1
        self.click_timer.start_timer()
        self.cubes[x][y].delete()
    
    def update(self):
        self.conway_timer.update()
        self.start_btn_timer.update()
        self.click_timer.update()

        for row in self.cubes:
            for cube in row:
                cube.update()

        if self.runGameOfLife and not self.conway_timer.start:
            self.conway_timer.start_timer()

        self.draw()

    def set_component(self,comp):
        self.component = comp
        self.draw_component = True

    def apply_component(self, component, i, j):
        comp_width, comp_height = component.width, component.height
        if self.click_timer.start:
            return
        if self.runGameOfLife:
            return
        if i < 0 or j < 0 or i >= self.rows or j >= self.cols:
            return -1
        if i + comp_width >= self.rows or j + comp_height >=self.cols:
            print('returned')
            return 
        
        struct = component.matrix 

        for a,row in enumerate(struct):
            for b,val in enumerate(row):
                if i+a >= self.rows or j+b >= self.cols:
                    pass
                self.cubes[i+a][j+b].value = val

        self.click_timer.start_timer()
        self.draw_component = False

    def toggle_red(self):
        for row in self.cubes:
            for cube in row:
                cube.toggle_red()


class Cube():
    def __init__(self, value, row, col, width, height, cols, rows, WIN):
        self.value = value
        self.nxt_val = 0

        self.row = row
        self.col = col

        self.width = width
        self.height = height

        self.cols = cols
        self.rows = rows

        rowGap = self.height / self.rows
        colGap = self.width / self.cols

        self.x = self.col * colGap
        self.y = self.row * rowGap

        self.WIN = WIN

        self.click_timer = Timer(0.15)

        self.set_color()
        self.show_red = True

    def draw(self):
        self.set_color()

        rowGap = self.height / self.rows
        colGap = self.width / self.cols

        x = self.col * colGap
        y = self.row * rowGap

        pygame.draw.rect(
            self.WIN, self.color, pygame.Rect(x, y, colGap, rowGap))


    def get_neighbours(self, board):
        total = 0
        x, y = self.row, self.col
        for i in range(max(0, x-1), min(self.rows, x+2)):
            for j in range(max(0, y-1), min(self.cols, y+2)):
                cube = board[i][j]
                if cube.value == 3:
                    total += 1

        if total == 1:
            return True
        if total == 2:
            return True

        return False

    def clicked(self):
        self.value += 1
        self.value %= 4
        self.set_color()

    def is_hovering(self) -> bool:
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        #Pos is the mouse position or a tuple of (x,y) coordinates
        pos = pygame.mouse.get_pos()
        return (
            pos[0] > self.x -0.1
            and pos[0] < self.x + colGap +0.1
            and pos[1] > self.y-0.1
            and pos[1] < self.y + rowGap +0.1
        )

    def update(self):
        pass
    
    def iter(self, board):
        # head -> tail
        if self.value == 3:
            self.nxt_val = 2
            return
        # tail -> conductor
        elif self.value == 2:
            self.nxt_val = 1
            return

        elif self.value == 1:
            self.nxt_val = 1
            # condoctor -> head
            if self.get_neighbours(board):
                self.nxt_val = 3
            return

        elif self.value == 0:
            self.nxt_val = 0

    def set_next(self):
        self.value = self.nxt_val
        self.set_color()

    def set_color(self):
        self.color = GREAY

        # condoctor
        if self.value == 1:
            self.color = YELLOW
        # electron tail 
        elif self.value == 2:
            if self.show_red:
                self.color = RED
            else:
                self.color = YELLOW
        # electron head
        elif self.value == 3:
            self.color = BLUE

    def delete(self):
        self.value -= 1
        self.value = abs(self.value)%4
        self.set_color()
    
    def reset(self):
        self.value = 0
        self.nxt_val = 0
        self.set_color()
    
    def toggle_red(self):
        self.show_red = not self.show_red

