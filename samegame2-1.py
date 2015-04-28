import random
import sys

class Game(object):
  def __init__(self, dimensions = (10,10), colorDistribution = [1,1,1,1]):
    self.cols, self.rows = dimensions
    self.board = self.genBoard(colorDistribution)
    
  def genBoard(self, colorDistribution):
    return ((1, 4, 3, 2, 3, 1, 3, 1, 3, 2),
            (1, 4, 3, 2, 2, 4, 2, 4, 4, 2), 
            (4, 3, 1, 3, 1, 1, 1, 3, 1, 2), 
            (2, 1, 2, 1, 3, 2, 4, 3, 2, 4), 
            (1, 4, 4, 4, 2, 1, 2, 3, 3, 1), 
            (3, 2, 2, 3, 3, 1, 2, 1, 4, 4), 
            (3, 3, 2, 2, 2, 3, 1, 2, 3, 3), 
            (3, 2, 2, 4, 4, 1, 3, 4, 1, 3), 
            (1, 2, 2, 4, 4, 2, 3, 1, 3, 3), 
            (2, 3, 4, 1, 3, 4, 3, 2, 4, 1),)
  
  def click(self,col,row):
    pts, self.board = self.floodfill(col,row, self.board[row][col], self.board)
    self.board = self.gravity(self.board)
    self.board = self.move(self.board)
    return pts
    
  
  def floodfill(self, col, row, color, board):
    value = board[row][col]
    if value != color or not(0 <= col < self.cols and 0 <= row < self.rows):
        return 0, board
    board = tuple([tuple([val if (x,y) != (col,row) else 0 for x,val in enumerate(line)]) for y,line in enumerate(board)])
    points1, board = self.floodfill(col, row+1, color, board)
    points2, board = self.floodfill(col, row-1, color, board)
    points3, board = self.floodfill(col+1, row, color, board)
    points4, board = self.floodfill(col-1, row, color, board)
    return sum([points1,points2,points3,points4]) + 1, board

  def gravity(self,board):
    return zip(*map(self.shift,zip(*board)))
    
  def shift(self, line):
    numbers = filter(bool,line)
    return tuple([0]*(len(line) - len(numbers)) + list(numbers))

  def move(self, board):
    cols = filter(lambda line: any(map(bool,line)),zip(*board))
    return tuple(zip(*(([0]*self.rows)*(len(cols)-self.cols)) + cols))
    
  def display(self):
    print "\n".join(map(lambda l:" ".join(map(str,l)), self.board))
    
