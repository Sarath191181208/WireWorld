import pygame 
from components.colors import *
import random
from components.timer import Timer 

def grab(win, x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    sub = win.subsurface(rect)
    surfce = pygame.Surface((width, height))
    surfce.blit(sub, (0,0))
    return surfce

class Grid():
    def __init__(self, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400, WIN=None):
        self.rows = cols
        self.cols = rows

        self.width, self.height = width, height
        self.WIN = WIN
        self.x, self.y = 0, 0
        self.surface = pygame.Surface((1000, 1000))
        self.offset_x, self.offset_y = 0, 0

        self.cubes = [
            [Cube(0, i, j, self.surface.get_width(), self.surface.get_height(), self.cols, self.rows, self.surface)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]

        self.runGameOfLife = False
        self.conway_timer = Timer(0.1, func=lambda:self.Conway(), loop=True)

        self.start_btn_timer = Timer(0.2)
        self.click_timer = Timer(0.15)

        self.draw_component = False
        self.component = None

        self.pan_selected = False
        self.pan_cord = None

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
        self.surface.fill(WHITE)

        rowGap = self.surface.get_height() / self.rows
        colGap = self.surface.get_width() / self.cols

        thick = 1

                # Draw Cubes
        for row in self.cubes:
            for cube in row:
                cube.draw(self.surface)

        for i in range(self.rows+1):
            pygame.draw.line(self.surface, BLACK, (0, i*rowGap),(self.surface.get_height(), rowGap*i), thick)

        for j in range(self.cols+1):
            pygame.draw.line(self.surface, BLACK, (j*colGap, 0), (colGap*j, self.surface.get_width()),thick)
        
        x_bound = max(0,min(self.offset_x,self.surface.get_width()-self.width))
        y_bound = max(0,min(self.offset_y,self.surface.get_height()-self.height))
        # print(x_bound, y_bound)
        blit_surface = grab(win=self.surface, x=x_bound, y=y_bound, width=self.width, height=self.height)
        win.blit(blit_surface, (0, 0))
        # win.blit(self.surface, (0,0))

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

    def clicked(self):
        x, y = pygame.mouse.get_pos()

        if x > self.width or x < self.x or y < self.y or y > self.height:
            return

        x += self.offset_x
        y += self.offset_y
    
        # x, y = pygame.mouse.get_pos()
        gap = self.surface.get_width() // self.rows
        y //= gap
        x //= gap

        i, j = y, x
        print(i, j)
    
        if self.click_timer.start:
            return
        if self.runGameOfLife:
            return

        if self.draw_component:

            self.apply_component(self.component, i, j)
            return
        if i < 0 or j < 0 or i >= self.rows or j >= self.cols:
            return -1
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

    def toggle_pan(self):
        self.pan_selected = not self.pan_selected
    
    def pan(self):
        if pygame.mouse.get_pressed()[0]:
            if self.pan_cord is None:
                self.pan_cord = pygame.mouse.get_pos()

            cord_x, cord_y = self.pan_cord 
            pos_x, pos_y = pygame.mouse.get_pos()

            delta_x, delta_y = cord_x-pos_x, cord_y-pos_y

            self.offset_x += delta_x
            self.offset_x = max(0, min(self.offset_x,self.surface.get_width()-self.width))
            self.offset_y += delta_y
            self.offset_y = max(0, min(self.offset_y,self.surface.get_height()-self.height))

        else:
            self.pan_cord = None
        
        
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

    def draw(self, win):
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

