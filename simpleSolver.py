#!/usr/bin/env python
from board import floodfill

def parseBoard():
  pass

def main():
  board = parseBoard()
  moves = []
  rows = len(board)
  cols = len(board[0])
  while(1):
    madeMove = False
    for x in range(cols):
      for y in range(rows):
        pts, newBoard = floodfill(board,board[x][y],x,y)
        if pts > 1:
          move.append((x,y))
          board = newBoard
          madeMove = True
          break
      if madeMove:
        break
    if not madeMove:
      break
  printMoves(moves)
  

if __name__ == "__main__":
  main()
