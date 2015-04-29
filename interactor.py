#!/usr/bin/env python
from subprocess import Popen, PIPE
from board import Board
from validator import getScore

def main():
  board = Board(colorDistribution = [1,1,1,1],seed=0xDEADBEEF).board
  proc = Popen("python simpleSolver.py",stdin=PIPE,stdout=PIPE,shell=True)
  proc.stdin.write(str(board) + "\n")
  proc.wait()
  output = proc.stdout.read()
  moves = eval(output)
  print getScore(board,moves)

if __name__ == "__main__":
  main()
