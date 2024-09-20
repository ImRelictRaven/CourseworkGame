import curses
import io

class myMenu:
    X = 10
    Y = 5
    ACTIVE = True
    SCR = None
    SHIFT_Y = 2
    SHIFT_X = 2
    MARGIN_X = 1
    MARGIN_Y = 1

    def __init__(self, level, func, name, tree, fullpath = ""):   # каждый элемент меню - сам меню и имеет функцию вызова при нажатии
                                # на вход подается дерево, каждый элемент которого состоит из тройки - текст, поддерево.
        self.level = level
        self.list = []
        self.name = name
        self.func = func
        self.active = 0
        self.width = 0
        self.height = len(tree)
        self.fullpath = fullpath + '-' + name
        
        for m in tree:
            self.list.append(myMenu(level+1, func, m[0], m[1], self.fullpath))
            if len(m[0]) > self.width:
                self.width = len(m[0])
        

    
    def run(self):
        snp = screen_dump(self.SCR)

        h = self.height + 2 * self.MARGIN_Y + 2 
        w = self.width + 2 * self.MARGIN_X + 2
        lux = self.X + self.level * self.SHIFT_X
        luy =  self.Y + self.level * self.SHIFT_Y

        sw = self.SCR.subwin(h, w, luy, lux)
        sw.clear()
        sw.refresh()
        
        self.draw_border()
        self.draw()
        
        while myMenu.ACTIVE:
            k = myMenu.SCR.getch()
            if k == 27:
                break
            elif k == curses.KEY_UP:
                if self.active != 0:
                    self.active -= 1
            elif k == curses.KEY_DOWN:
                if self.active != len(self.list) - 1:
                    self.active += 1
            elif k == curses.KEY_ENTER or k == 10 or k == 13:
                myMenu.ACTIVE = self.func(self.fullpath + '-' + self.list[self.active].name)
                if self.list[self.active].list != []:
                    self.list[self.active].run()

            self.draw()
        
        load_dump(self.SCR, snp)
        self.SCR.refresh()
        
    def draw(self):
        i = 0
        for m in self.list:
            x = myMenu.X + self.level * myMenu.SHIFT_X + 1 + self.MARGIN_X
            y = myMenu.Y + self.level * myMenu.SHIFT_Y + 1 + self.MARGIN_Y
            if self.active == i:
                attr = curses.A_REVERSE
            else:
                attr = 0
            myMenu.SCR.addstr(y + i, x, m.name, attr)
            i += 1

    def draw_border(self):
        x1 = myMenu.X + self.level * myMenu.SHIFT_X
        y1 = myMenu.Y + self.level * myMenu.SHIFT_Y
        x2 = x1 + self.width + 2 * self.MARGIN_X + 2
        y2 = y1 + self.height + 2 * self.MARGIN_Y + 2

        for i in range(x1, x2, 1):
            self.SCR.addch(y1, i, curses.ACS_BLOCK)
            self.SCR.addch(y2, i, curses.ACS_BLOCK)
        for i in range(y1, y2 + 1, 1):
            self.SCR.addch(i, x1, curses.ACS_BLOCK)
            self.SCR.addch(i, x2, curses.ACS_BLOCK)


def screen_dump(scr):
    a = []
    rows, cols = scr.getmaxyx()
    for i in range(rows):
        for j in range(cols):
            a.append(scr.inch(i,j))
    return a

def load_dump(scr, dump):
    rows, cols = scr.getmaxyx()
    for i in range(len(dump)-1):
        scr.addch(int(i/cols), i % cols, dump[i])
    scr.refresh()
    
