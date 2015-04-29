#!/usr/bin/env python
import board

def main():
#for test purposes
  inp = input()
  b = board.Board(board=((1, 4, 3, 2, 3, 1, 3, 1, 3, 2),(1, 4, 3, 2, 2, 4, 2, 4, 4, 2), (4, 3, 1, 3, 1, 1, 1, 3, 1, 2), (2, 1, 2, 1, 3, 2,4,3, 2, 4), (1, 4, 4, 4, 2, 1, 2, 3, 3, 1), (3, 2, 2, 3, 3, 1, 2, 1, 4, 4), (3, 3, 2, 2, 2, 3, 1, 2, 3, 3), (3, 2, 2, 4, 4, 1, 3, 4, 1, 3), (1, 2, 2, 4, 4, 2, 3, 1, 3, 3), (2, 3, 4, 1, 3, 4, 3, 2, 4, 1),))
  for m in inp:
    b.display()
    print "move: ", str(m)
    print "score: ", b.click(*m)
  b.display()
#for test

if __name__ == "__main__":
  main()
