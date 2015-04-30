#!/usr/bin/env python
from core import Game

def getScore(board, moves):
  score = 0
  b = Board(board=board)
  for m in moves:
    score += b.click(*m)
  return score


def main():
  board = input()
  moves = input()
  getScore(b,moves)

if __name__ == "__main__":
  main()
