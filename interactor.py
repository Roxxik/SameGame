#!/usr/bin/env python
from subprocess import Popen, PIPE
from board import Board
from validator import getScore

def interact(prog, board):
  try:
    proc = Popen(prog,stdin=PIPE,stdout=PIPE,shell=True)
    proc.stdin.write(str(board) + "\n")
    proc.wait()
    return eval(proc.stdout.read())
  except:
    return None  

def main():
  board = Board(colorDistribution = [1,1,1,1],seed=0xDEADBEEF).board
  moves = interact("python simpleSolver.py",board)
  if moves != None:
    print getScore(board,moves)
  else:
    print "error"

if __name__ == "__main__":
  main()
