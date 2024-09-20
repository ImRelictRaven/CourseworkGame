import curses
from Snake import mySnake 
import time
from menu import myMenu

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)

    x_b = (0, 20)
    y_b = (0, 19)
    snake  = mySnake(stdscr, 10, 10, y_b, x_b)
    snake.run()

curses.wrapper(main) 