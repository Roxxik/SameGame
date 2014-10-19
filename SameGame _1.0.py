import random
import re
import sys
from colorama import init, Fore, Back, Style
init()

class Cgame:
# initializes a gameboard
# containing boardheight (self.row), boardwidth (self.col), blocks placed on the board (self.board)
  def __init__ (self, dimensions = (10,10), colorDistribution = [1,1,1,1]):
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
      for (column, row) in coords[:coloredAmount]:
        self.board[column][row] = colorNum
      colorNum+=1
      coords = coords[coloredAmount:]
    colorNum = 1
    for (column, row) in coords:
      self.board[column][row] = colorNum
      colorNum+=1 
     
# simulates a click on the board, destroying the block of stones
# applying gravity
# returns the amount of stones destroyed
  def click(self, column, row):
    deleteCoords = [(column, row)]
    deleteCoords = self.spread(deleteCoords, column, row, self.board[column][row])
    if len(deleteCoords) > 1:
      for delete in deleteCoords:
        column, row = delete
        self.board[column][row] = 0
      self.gravityDown()
      self.gravityLeft()
    return len(deleteCoords)
      
# recursive algorithm to determine the stones to destroy
# returns a list of coordinates, each coordinate represents a stone to destroy
  def spread(self, deleteCoords, column, row, colorNum):
    surroundings = [(column-1, row), (column, row-1), (column, row+1), (column+1, row)]
    for nextBlock in surroundings:
      nextCol, nextRow = nextBlock
      if (0 <= nextCol < self.row):
        if (0 <= nextRow < self.col):
          if (nextBlock not in deleteCoords):
            if  (self.board[nextCol][nextRow] == colorNum):
              deleteCoords = self.spread([nextBlock] + deleteCoords, nextCol, nextRow, colorNum)
    return deleteCoords

# applies downwards gravity
  def gravityDown(self):
    for column in self.board:
      for row in range(self.row):
        if column[row] == 0:
          column.pop(row)
          column.insert(0, 0)
     
# applies leftwards gravity
# if a column is empty, it'll be deleted and an empty one will be inserted on the left side   
  def gravityLeft(self):
    for column in range(self.col):
      empty = True
      
      for row in self.board[column]:
        if row != 0:
          empty = False
          
      if empty:
        print(str(column))
        self.print()
        self.board.pop(column)
        emptyCol = []
        for row in range(self.row):
          emptyCol.append(0)
        self.board.insert(0, emptyCol)
      
# prints a gameboard
# includes the colorama-library to display colors on windows
  def print (self):
    for row in range(self.row):
      sys.stdout.write('[')
      for column in range(self.col):
        colorNum = self.board[column][row]
        if colorNum == 0:
          sys.stdout.write(Back.BLACK + str(colorNum) + Back.RESET)
        elif colorNum == 1:
          sys.stdout.write(Back.RED + str(colorNum) + Back.RESET)
        elif colorNum == 2:
          sys.stdout.write(Back.GREEN + str(colorNum) + Back.RESET)
        elif colorNum == 3:
          sys.stdout.write(Back.YELLOW + Fore.BLACK + str(colorNum) + Back.RESET + Fore.RESET)
        elif colorNum == 4:
          sys.stdout.write(Back.BLUE + str(colorNum) + Back.RESET)
        elif colorNum == 5:
          sys.stdout.write(Back.MAGENTA + str(colorNum) + Back.RESET)
        elif colorNum == 6:
          sys.stdout.write(Back.CYAN + str(colorNum) + Back.RESET)
        else:
          sys.stdout.write(Back.WHITE + str(colorNum) + Back.RESET)
          
        if column < self.col-1:
          sys.stdout.write(', ')
      print(']')
    print()

# shuffles the given list
def shuffle(list): 
  for i in range (len(list)):
    j = random.randint(0, i)
    list[i], list[j] = list[j], list[i]
  return list  
  
# Points: You don't get points for 2 destroyed Stones.
# 3 destroyed Stones gain 1 Point and every additional Stone will gain additional 2 Points
# e.g. 4th destroyed Stone = 3 Pts., 5th destroyed Stone = 5 Pts., a.s.o
# shortens into: ((amount of stones) - 2) ^ 2)
def calcPoints(amount):
  if amount <= 2:
    return 0
  else:
    return pow(amount-2, 2)    
  
# creates a new board
# then repeatetly asks for coordinates as input (checking if valid)
def main():
  game = Cgame()
  game.print()
  pattern = re.compile(r"(\d*),(\d*)")
  points = 0
  rounds = 0
  while True:
    coords = input()
    match = re.match(pattern, coords)
    if match != None:
      column = int(match.group(1))
      row = int(match.group(2))
      if (column < game.col) and (row < game.row):
        points += calcPoints(game.click(column, row))
        rounds += 1
        print()
        game.print()
        print('Punkte: ' + str(points))
        print('Runden: ' + str(rounds))
        print()
if __name__ == "__main__":
  main()
