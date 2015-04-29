#!/usr/bin/env python
from board import Board

def getScore(board, moves):
  score = 0
  b = Board(board=board)
  for m in moves:
    score += b.click(*m)
  b.display()
  print score


def main():
  board = input()
  moves = input()
  getScore(b,moves)

if __name__ == "__main__":
  main()
