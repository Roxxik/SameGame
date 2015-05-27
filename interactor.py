#!/usr/bin/env python
from subprocess import Popen, PIPE
from core import Game
from validator import evaluate
from time import clock

def interact(prog, board):
    res = None
    try:
        proc = Popen(prog,stdin=PIPE,stdout=PIPE,shell=True)
        #(out,err) = proc.communicate(str(board) + "\n")
        proc.stdin.write(str(board) + "\n")
        start = clock()
        proc.stdin.close()
        while(1):
            if (clock() - start) * 1000 > 1:
                proc.terminate()
                break;
            res = eval(proc.stdout.readline())
    except:
        pass 
    return res

def main():
  raw_board = input()
  board = list(reversed(raw_board))
  moves = interact("~/git/samegameSolver/c/2.0/solver",raw_board)
  if moves != None:
    print "moves:", len(moves)
    print moves
    print "score:", evaluate(board,moves), "py"
  else:
    print "error"

if __name__ == "__main__":
  main()
