import random
import re

class Cgame:
  def __init__ (self, dimensions = (100,100), colorDistribution = [1,1,1,1]):
    col, row = dimensions
    self.row = row
    self.col = col
    fields = col*row
    colors = sum(colorDistribution)
    coords = shuffle([(i,j) for j in range (col) for i in range (row)])
    colorNum = 1
    self.board = [[0 for j in range (col)] for i in range (row)]
    for color in colorDistribution:
      coloredAmount = fields * color // colors
      for (x,y) in coords[:coloredAmount]:
        self.board[x][y] = colorNum
      colorNum+=1
      coords = coords[coloredAmount:]
    colorNum = 1
    for (x,y) in coords:
      self.board[x][y] = colorNum
      colorNum+=1 
      
  def click(self, x, y):
    deleteCoords = [(x,y)]
    deleteCoords = self.spread(deleteCoords, x, y, self.board[x][y])
    print(deleteCoords)
    for delete in deleteCoords:
      x,y = delete
      self.board[x][y] = 0
      
  def spread(self, deleteCoords, x, y, colorNum):
    surroundings = [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]
    for nextBlock in surroundings:
      i, j = nextBlock
      if (0 <= i < self.row):
        if (0 <= j < self.col):
          if (nextBlock not in deleteCoords):
            if  (self.board[i][j] == colorNum):
              deleteCoords = self.spread([nextBlock] + deleteCoords, i, j, colorNum)
    return deleteCoords
      
  def print (self):
    for row in self.board:
      print (row)

def shuffle(list): 
  for i in range (len(list)):
    j = random.randint(0, i)
    list[i], list[j] = list[j], list[i]
  return list  
  
def main():
  game = Cgame()
  game.print()
  pattern = re.compile(r"(\d*),(\d*)")
  while True:
    coords = input()
    match = re.match(pattern, coords)
    if match != None:
      x, y = match.group(1,2)
      game.click(int(x), int(y))
      game.print()
if __name__ == "__main__":
  main()
