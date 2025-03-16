import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        cols = 12
        rows = 10
        m1 = Maze(0,0,rows,cols,10,10)
        self.assertEqual(len(m1._cells),cols)
        self.assertEqual(len(m1._cells[0]),rows)

if __name__ == "__main__":
    unittest.main()