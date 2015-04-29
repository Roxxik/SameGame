import random

#todo consider replacing this by a self written prng(e.g. lfsr)
def shuffle(list, seed=None):
  if seed != None:
    random.seed(seed)
  for i in range (len(list)):
    j = random.randint(0, i)
    list[i], list[j] = list[j], list[i]
  return list  

class Game(object):
  def __init__(self, dimensions = (10,10), colorDistribution = [1,1,1,1], seed = None):
    self.cols, self.rows = dimensions
    self.board = self.genBoard(colorDistribution, seed)
    
  """    
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
  
  def click(self,col,row):
    if 0 <= col < self.cols and 0 <= row < self.rows:
      blocks, board = self.floodfill(col,row, self.board[row][col], self.board)
      if blocks > 1:
        self.board = self.move(self.gravity(board))
      return blocks
    else:
      return 0
  
  def floodfill(self, col, row, color, board):
    if color == 0 or not(0 <= col < self.cols and 0 <= row < self.rows):
      return 0, board
    value = board[row][col]
    if value != color:
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
    return tuple(zip(*(cols + ([([0]*self.rows)]*(self.cols-len(cols))))))
    
  def display(self):
    print "\n".join(map(lambda l:" ".join(map(str,l)), self.board))
    
