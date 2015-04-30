#!/usr/bin/env python
from core import floodfill, gravity, move

def parseBoard():
  return input()

def printMoves(moves):
  print moves

def getSolution(board):
  moves = []
  rows = len(board)
  cols = len(board[0])
  while(1):
    madeMove = False
    for x in range(cols):
      for y in range(rows):
        pts, newBoard = floodfill(board,board[y][x],x,y)
        if pts > 1:
          moves.append((x,y))
          board = move(gravity(newBoard))
          madeMove = True
    if not madeMove:
      break
  return moves

def main():
  board = parseBoard()
  moves = getSolution(board)
  printMoves(moves)


if __name__ == "__main__":
  main()
