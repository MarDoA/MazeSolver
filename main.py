from window import *
from maze import *

def main():
    win = Window(800, 600)

    maze = Maze(20,20,10,8,30,40,win)
    maze._break_walls(0,0)

    maze._reset_visited()
    maze.solve_r(0,0)

    win.wait_for_close()



main()