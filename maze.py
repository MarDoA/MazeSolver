from window import Line,Point
from time import sleep
import random

class Cell():
    def __init__(self, x1, x2, y1, y2, win=None, has_left=True, has_right=True, has_top=True, has_bottom=True):
        self.has_left = has_left
        self.has_right = has_right
        self.has_top = has_top
        self.has_bottom = has_bottom
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
        self.center_x = ((x2 - x1)/2) + x1
        self.center_y = ((y2 - y1)/2) + y1
        self.win = win
        self.visited = False
    
    def draw(self):
        if self.win is None:
            return

        bcolor = "white"
        if self.has_top:
            bcolor = "black"
        self.win.canvas.create_line(self.x1,self.y1,self.x2,self.y1,fill=bcolor,width=2)
        
        lcolor = "white"
        if self.has_left:
            lcolor = "black"    
        self.win.canvas.create_line(self.x1,self.y1,self.x1,self.y2,fill=lcolor,width=2)
        
        rcolor = "white"
        if self.has_right:
            rcolor = "black"
        self.win.canvas.create_line(self.x2,self.y1,self.x2,self.y2,fill=rcolor,width=2)
        
        tcolor = "white"
        if self.has_bottom:
            tcolor = "black"
        self.win.canvas.create_line(self.x1,self.y2,self.x2,self.y2,fill=tcolor,width=2)

    def draw_move(self, to_cell, undo=False):
        dline = Line(Point(self.center_x,self.center_y),Point(to_cell.center_x,to_cell.center_y))
        if undo:
            dline.draw(self.win.canvas, "grey")
        else:
            dline.draw(self.win.canvas, "red")


class Maze():
    def __init__(self, x1, y1, nrows, ncols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.nrows = nrows
        self.ncols = ncols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed:
            random.seed(seed)
        self.seed = seed
        self._cells = []
        self._create_cells()
        
    def _create_cells(self):
        for i in range(self.ncols):
            coloumn = []
            for j in range(self.nrows):
                c = self._draw_cell(i,j)
                coloumn.append(c)
                self._animate()
            self._cells.append(coloumn)
        self._break_entrance_exit()

    def _draw_cell(self, i, j):
        x1 = (i * self.cell_size_x) + self.x1
        x2 = ((i+1) * self.cell_size_x) + self.x1
        y1 = (j * self.cell_size_y) + self.y1
        y2 = ((j+1) * self.cell_size_y) + self.y1

        cel = Cell(x1,x2,y1,y2,self.win)
        cel.draw()
        return cel

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        sleep(0.05)

    def _break_entrance_exit(self):
        entrance = self._cells[0][0]
        entrance.has_top = False
        entrance.draw()
        exit = self._cells[-1][-1]
        exit.has_bottom = False
        exit.draw()

    def _reset_visited(self):
        for col in self._cells:
            for c in col:
                c.visited = False
        
    def _break_walls(self,i,j):
        cell = self._cells[i][j]
        cell.visited = True
        while True:
            to_visit = []
            #left and right
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1,j))
            if i < self.ncols-1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1,j))
            #top and bottom
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i,j-1))
            if j < self.nrows-1 and not self._cells[i][j+1].visited:
                to_visit.append((i,j+1))
            
            if len(to_visit) == 0:
                self._cells[i][j].draw()
                self._animate()
                return
            dir = to_visit[random.randrange(len(to_visit))]
            if dir[0] == i+1:
                self._cells[i][j].has_right = False
                self._cells[dir[0]][dir[1]].has_left = False
            elif dir[0] == i-1:
                self._cells[i][j].has_left = False
                self._cells[dir[0]][dir[1]].has_right = False
            elif dir[1] == j+1:
                self._cells[i][j].has_bottom = False
                self._cells[dir[0]][dir[1]].has_top = False
            elif dir[1] == j-1:
                self._cells[i][j].has_top = False
                self._cells[dir[0]][dir[1]].has_bottom = False
            self._break_walls(*dir)
    
    def solve_r(self,i,j):
        self._animate()
        self._cells[i][j].visited = True

        if i == self.ncols-1 and j == self.nrows-1:
            return True
        
        if not self._cells[i][j].has_right and not self._cells[i+1][j].visited:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self.solve_r(i+1,j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j],True)
            
        if not self._cells[i][j].has_left and not self._cells[i-1][j].visited:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self.solve_r(i-1,j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j],True)


        if j>0 and not self._cells[i][j].has_top and not self._cells[i][j-1].visited:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self.solve_r(i,j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1],True)
            
            
        if not self._cells[i][j].has_bottom and not self._cells[i][j+1].visited:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self.solve_r(i,j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1],True)
        return False
                

        




            
            


                
