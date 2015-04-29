import random

def shuffle(list, seed=None):
  if seed != None:
    random.seed(seed)
  #Fisher-Yates-Algorithm
  for i in range (len(list)):
    j = random.randint(0, i)
    list[i], list[j] = list[j], list[i]
  return list  

def transpose(list):
  return zip(*list)

class Game(object):
  #important note:
  #while programming this the board ought to be immutable to keep a functional style
  #therefor the board is a tuple instead of a list
  #might be changed later for performance reasons
  def __init__(self, dimensions = (10,10), colorDistribution = [1,1,1,1], seed = None):
    self.cols, self.rows = dimensions
    self.board = self.genBoard(colorDistribution, seed)
    
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
  """
  #generate a board
  #@param colorDistibution The distribution of colors, the index is the color the value is the amount
  #@param seed The seed to initialize the pnrg
  #@return The generated board
  def genBoard(self, colorDistribution, seed=None):
    colorSum = sum(colorDistribution)
    coords = shuffle([(i,j) for i in range (self.cols) for j in range (self.rows)], seed)
    board = [[0 for i in range (self.cols)] for j in range (self.rows)]
    fields = self.cols * self.rows
    for color, colorAmount in enumerate(colorDistribution, start = 1):
      coloredFields = fields * colorAmount // colorSum
      for (col, row) in coords[:coloredFields]:
        board[col][row] = color
      coords = coords[coloredFields:]
    for color, (col, row) in enumerate(coords,start=1):
      board[col][row] = color
    return board
  
  #clicks on the board of the Game
  #@param col, row The coords to click at
  #@return The number of blocks destroyed
  def click(self,col,row):
    if 0 <= col < self.cols and 0 <= row < self.rows:
      pts, board = self.floodfill(self.board, self.board[row][col], col,row)
      if pts > 1:
        self.board = self.move(self.gravity(board))
      return pts
    else:
      return 0
  
  #Floodfills the board with zeros startign at position col,row
  #@param IN board The board to apply the floodfill to
  #@param IN color The color that is to be replaced
  #@param col The x-coordinate to start at
  #@param row The y-coordinate to start at
  #@return (The number of blcks destroyed, The floodfilled board)
  def floodfill(self, board, color, col, row):
    if color == 0 or not(0 <= col < self.cols and 0 <= row < self.rows):
      return 0, board
    value = board[row][col]
    if value != color:
      return 0, board
    board = tuple([tuple([val if (x,y) != (col,row) else 0 for x,val in enumerate(line)]) for y,line in enumerate(board)])
    downPts , board = self.floodfill(board, color, col, row+1)
    upPts   , board = self.floodfill(board, color, col, row-1)
    rightPts, board = self.floodfill(board, color, col+1, row)
    leftPts , board = self.floodfill(board, color, col-1, row)
    return sum([downPts,upPts,rightPts,leftPts]) + 1, board
  
  #apply gravity to the board
  #@param IN board The board to apply the gravity to
  #@return The board with the applied gravity
  def gravity(self,board):
    #for Haskellers:
    #gravity = transpose . map shift . transpose
    return transpose(map(self.shift,transpose(board)))
  
  #apply gravity to a single column
  #@param IN line The column to apply the gravity to
  #@return The column with the applied gravity
  def shift(self, line):
    #filter out Zeros and fill the line to its previous size with zeros up front
    numbers = filter(bool,line)
    return tuple([0]*(len(line) - len(numbers)) + list(numbers))
  
  #moves empty columns to the right
  #@param IN board The board to apply the move to
  #@returnThe board with the applied move
  def move(self, board):
    #filter out all only-zero-columns and fill the board to its previous size with only-zero-columns to the left
    cols = filter(lambda line: any(map(bool,line)),transpose(board))
    return tuple(transpose(cols + ([([0]*self.rows)]*(self.cols-len(cols)))))
  
  #print the board
  def display(self):
    print "\n".join(map(lambda l:" ".join(map(str,l)), self.board))
    
