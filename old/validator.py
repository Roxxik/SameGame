#!/usr/bin/env python
from core import Game
from itertools import chain
from collections import Counter

def getScore(n):
    return (n-1)**2

def penalty(board):
    return sum(map(getScore,filter(bool,Counter(filter(bool,chain(*board))).values())))

def evaluate(board, moves):
    score = 0
    b = Game(board=board)
    b.display()
    for m in moves:
        score += getScore(b.click(*m))
        print m
        print score
        b.display()
    print "score", score
    print "penalty", penalty(b.board)
    score -= penalty(b.board)
    b.display()
    return score


def main():
    board = input()
    moves = input()
    print evaluate(board,moves)

if __name__ == "__main__":
    main()
