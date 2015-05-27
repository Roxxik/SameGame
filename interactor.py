from subprocess import Popen, PIPE
from time import sleep, clock
from sys import argv, exit

def interact(prog, board):
    res = None
    try:
        proc = Popen(prog,stdin=PIPE,stdout=PIPE,shell=True)
        sleep(5)
        start = clock()
        proc.stdin.write(str(board) + "\n")
        proc.stdin.close()
        while(1):
            res = eval(proc.stdout.readline())
            if (clock() - start) * 1000 > 1:
                proc.terminate()
                break
    except:
        pass
    return res

def validate(prog,board,moves):
    try:
        proc = Popen(prog,stdin=PIPE,stdout=PIPE,shell=True)
        (out,err) = proc.communicate(str(board) + "\n" + str(moves) + "\n")
        return eval(out)
    except:
        return None

def main():
    if len(argv) < 3:
        print "wrong number of arguments"
        exit(1)
    board = input()
    player = argv[1]
    moves = interact(player,board)
    if moves == None:
        print "something went wrong"
        exit(1)
    print "moves: ", len(moves)
    print moves
    validator = argv[2]
    (endBoard,score) = validate(validator, board, moves)
    print "score: " score
    print "finalBoard: "
    printBoard(endBoard)
    exit(0)
