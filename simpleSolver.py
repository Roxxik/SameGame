#!/usr/bin/env python
from board import floodfill, gravity, move, genBoard

def parseBoard():
  return input()

def printMoves(moves):
  print moves

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
          moves.append((x,y))
          board = move(gravity(newBoard))
          madeMove = True
          break
      if madeMove:
        break
    if not madeMove:
      break
  printMoves(moves)
  

if __name__ == "__main__":
  main()
