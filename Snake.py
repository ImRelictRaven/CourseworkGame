import curses
import time
import random
from menu import myMenu
import io



class mySnake:
    def __init__(self, stdscr, y, x, y_bound, x_bound):
        self.scr = stdscr
        self.points = [(y, x)] # точки змеи
        self.speed = 3 # скорость по дефолту
        self.quit_game = False # признак окончания игры
        self.direction = (1, 0) # направление движения змеи по дефолту
        self.char = ord('o') # символ туловища змеи
        self.border_char = curses.ACS_BLOCK # символ из которого рисуем рамку
        self.food_char = 'X'
        self.y_bound = y_bound # y_bound - кортеж из минимального и максимального y
        self.x_bound = x_bound # x_bound- кортеж из минимального и максимального x
        
        myMenu.SCR = stdscr
        a = [["New Game", []], \
             ["Settings", [ \
                 ["Speed", [ \
                     ["1", []], \
                     ["2", []], \
                     ["3", []] \
                     ]], \
                 ["Snake symbol", [\
                     ["o", []], \
                     ["#", []], \
                     [chr(9830), []] \
                     ]], \
                 ["Food symbol", [ \
                     ["X", []], \
                     ["D", []], \
                     [chr(9829), []] \
                     ]], \
                 ]], \
             ["Quit",[]]]
        self.mnu = myMenu(0, self.menu_func, "", a)

        
        random.seed()
        curses.resize_term(y_bound[1]+1, x_bound[1]+20)
        self.score = 0
        self.new_food()
        self.draw_boarder()
        self.redraw()


        
    def new_food(self):
        while True:
            yy = random.randint(self.y_bound[0]+1, self.y_bound[1]-1)
            xx = random.randint(self.x_bound[0]+1, self.x_bound[1]-1)
            if (yy, xx) not in self.points:
                break
        self.scr.addch(yy, xx, self.food_char)
        self.food = (yy, xx)

    def redraw(self):
        self.scr.clear()
        self.scr.addch(self.food[0], self.food[1], self.food_char)    
        self.draw_boarder()
        self.redraw_score()
        for p in self.points:
            self.scr.addch(p[0], p[1], self.char)
        self.scr.refresh()

    def redraw_score(self):
        self.scr.addstr(3, self.x_bound[1] + 6, "Score: " + str(self.score))

    def draw_boarder(self):
        self.scr.hline(self.y_bound[0], self.x_bound[0], self.border_char, self.x_bound[1] - self.x_bound[0])
        self.scr.hline(self.y_bound[1], self.x_bound[0], self.border_char, self.x_bound[1] - self.x_bound[0])
        self.scr.vline(self.y_bound[0], self.x_bound[0], self.border_char, self.y_bound[1] - self.y_bound[0])
        self.scr.vline(self.y_bound[0], self.x_bound[1], self.border_char, self.y_bound[1] - self.y_bound[0] + 1)

    def move(self):
        head = self.points[-1]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        if self.scr.inch(new_head[0], new_head[1]) in [self.border_char, self.char]:
            return False

        self.points.append(new_head)
        self.scr.addch(new_head[0], new_head[1], self.char)
        if (self.points[-1][0] != self.food[0]) or (self.points[-1][1] != self.food[1]):
            self.scr.addch(self.points[0][0], self.points[0][1], ' ')
            
            self.points.pop(0)
        else:
            self.score += 1
            self.redraw_score()
            self.new_food()
        self.scr.refresh()
        return True

    def run(self):
        self.scr.nodelay(1)
        while not self.quit_game:
            self.redraw()
            while self.move() and not self.quit_game:
                if self.direction[0] == 0:
                    time.sleep(0.3 / self.speed)
                else:
                    time.sleep(0.45 / self.speed)
                k = self.scr.getch()
                if k == 27:
                    myMenu.ACTIVE = True
                    self.mnu.run()
                    self.redraw()

                elif k == curses.KEY_RIGHT:
                    self.direction = (0, 1)
                elif k == curses.KEY_LEFT:
                    self.direction = (0, -1)
                elif k == curses.KEY_UP:
                    self.direction = (-1, 0)
                elif k == curses.KEY_DOWN:
                    self.direction = (1, 0)
                elif k == ord(' '):
                    self.pause()
                    self.redraw()
            self.scr.addstr(int((self.y_bound[1]+self.y_bound[0])/2), int((self.x_bound[1]+self.x_bound[0])/2) - 4, "Game over", curses.A_REVERSE)
            self.scr.refresh()
            self.scr.nodelay(0)
            k = -1
            while k != 10:
                k = self.scr.getch()
            myMenu.ACTIVE = True
            self.mnu.run()
        

    def pause(self):
        self.scr.nodelay(0)
        self.scr.addstr(int((self.y_bound[1]+self.y_bound[0])/2), int((self.x_bound[1]+self.x_bound[0])/2) - 2, "Pause", curses.A_REVERSE)
        while self.scr.getch() != ord(' '):
            k = 0
        self.scr.refresh()           
        self.scr.nodelay(1)
    

    def menu_func(self, path):
        if path == "--Quit":
            self.quit_game = True
        elif path == "--New Game":
            self.points = [(10, 10)]
            self.score = 0
            self.new_food()
            self.quit_game = False
            self.scr.nodelay(1)
        elif path == "--Settings-Speed-1":
            self.speed = 1
        elif path == "--Settings-Speed-2":
            self.speed = 2
        elif path == "--Settings-Speed-3":
            self.speed = 3
        elif path == "--Settings-Snake symbol-o":
            self.char = 'o'
        elif path == "--Settings-Snake symbol-#":
            self.char = '#'
        elif path == "--Settings-Snake symbol-" + chr(9830):
            self.char = 9830
        elif path == "--Settings-Food symbol-" + chr(9829):
            self.food_char = 9829
        elif path == "--Settings-Food symbol-X":
            self.food_char = 'X'
        elif path == "--Settings-Food symbol-D":
            self.food_char = 'D'
        else:
            return True        
        

        return False