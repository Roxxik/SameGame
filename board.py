#! /usr/bin/env python
import random

def shuffle(list, seed=None):
  if seed != None:
    random.seed(seed)
  #Fisher-Yates-Algorithm
  for i in range (len(list)):
    j = random.randint(0, i)
    list[i], list[j] = list[j], list[i]
  return list  

"""for test purposes:
def genBoard(self, colorDistribution, seed=None):
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

same but without \n
((1, 4, 3, 2, 3, 1, 3, 1, 3, 2),(1, 4, 3, 2, 2, 4, 2, 4, 4, 2), (4, 3, 1, 3, 1, 1, 1, 3, 1, 2), (2, 1, 2, 1, 3, 2,4,3, 2, 4), (1, 4, 4, 4, 2, 1, 2, 3, 3, 1), (3, 2, 2, 3, 3, 1, 2, 1, 4, 4), (3, 3, 2, 2, 2, 3, 1, 2, 3, 3), (3, 2, 2, 4, 4, 1, 3, 4, 1, 3), (1, 2, 2, 4, 4, 2, 3, 1, 3, 3), (2, 3, 4, 1, 3, 4, 3, 2, 4, 1),)

simple solver solution
[(0, 0), (0, 5), (0, 6), (0, 7), (0, 8), (1, 6), (1, 8), (1, 9), (2, 4), (2, 5), (2, 6), (2, 8), (4, 4), (4, 7), (5, 1), (5, 2), (5, 4), (5, 6), (6, 5), (6, 6), (6, 8), (6, 9), (7, 7), (0, 9), (2, 6)]
"""
#generate a board
#@param colorDistibution The distribution of colors, the index is the color the value is the amount
#@param seed The seed to initialize the pnrg
#@return The generated board
def genBoard(cols, rows, colorDistribution, seed=None):
  colorSum = sum(colorDistribution)
  coords = shuffle([(i,j) for i in range (cols) for j in range (rows)], seed)
  board = [[0 for i in range (cols)] for j in range (rows)]
  fields = cols * rows
  for color, colorAmount in enumerate(colorDistribution, start = 1):
    coloredFields = fields * colorAmount // colorSum
    for (col, row) in coords[:coloredFields]:
      board[col][row] = color
    coords = coords[coloredFields:]
  for color, (col, row) in enumerate(coords,start=1):
    board[col][row] = color
  return board

#Floodfills the board with zeros startign at position col,row
#@param IN board The board to apply the floodfill to
#@param IN color The color that is to be replaced
#@param col The x-coordinate to start at
#@param row The y-coordinate to start at
#@return (The number of blcks destroyed, The floodfilled board)
def floodfill(board, color, col, row):
  if color == 0 or not(0 <= col < len(board[0]) and 0 <= row < len(board)):
    return 0, board
  value = board[row][col]
  if value != color:
    return 0, board
  board = tuple([tuple([val if (x,y) != (col,row) else 0 for x,val in enumerate(line)]) for y,line in enumerate(board)])
  downPts , board = floodfill(board, color, col, row+1)
  upPts   , board = floodfill(board, color, col, row-1)
  rightPts, board = floodfill(board, color, col+1, row)
  leftPts , board = floodfill(board, color, col-1, row)
  return sum([downPts,upPts,rightPts,leftPts]) + 1, board


def transpose(list):
  return zip(*list)

#apply gravity to the board
#@param IN board The board to apply the gravity to
#@return The board with the applied gravity
def gravity(board):
  #for Haskellers:
  #gravity = transpose . map shift . transpose
  return transpose(map(shift,transpose(board)))

#apply gravity to a single column
#@param IN line The column to apply the gravity to
#@return The column with the applied gravity
def shift(line):
  #filter out Zeros and fill the line to its previous size with zeros up front
  numbers = filter(bool,line)
  return tuple([0]*(len(line) - len(numbers)) + list(numbers))

#moves empty columns to the right
#@param IN board The board to apply the move to
#@returnThe board with the applied move
def move(board):
  #filter out all only-zero-columns and fill the board to its previous size with only-zero-columns to the left
  cols = filter(lambda line: any(map(bool,line)),transpose(board))
  return tuple(transpose(cols + ([[0]*len(board[0])]*(len(board)-len(cols)))))



class Board(object):
  #important note:
  #while programming this the board ought to be immutable to keep a functional style
  #therefor the board is a tuple instead of a list
  #might be changed later for performance reasons
  def __init__(self, dimensions = (10,10), colorDistribution = [1,1,1,1], seed = None, board = None):
    if board != None:
      self.board = board
      self.rows = len(board)
      self.cols = len(board[0])
    else:
      self.cols, self.rows = dimensions
      self.board = genBoard(self.cols, self.rows, colorDistribution, seed)
  
  #clicks on the board of the Game
  #@param col, row The coords to click at
  #@return The number of blocks destroyed
  def click(self,col,row):
    if 0 <= col < self.cols and 0 <= row < self.rows:
      pts, board = floodfill(self.board, self.board[row][col], col,row)
      if pts > 1:
        self.board = move(gravity(board))
      return pts
    else:
      return 0

  
  #print the board
  def display(self):
    print "\n".join(map(lambda l:" ".join(map(str,l)), self.board))
