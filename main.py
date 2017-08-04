print('The worst chess engine in the world!')

import chess, chess.svg
import sys
import evaluation

board = chess.Board()

cpuColor = chess.BLACK

positions = 0

def calculateBestMove(depth):
    global positions
    positions = 0
    legalMoves = board.legal_moves
    bestMove = None
    
    #use any negative large number
    maxScore = -evaluation.INFINITY

    for move in legalMoves:
        board.push(move)

        score = -negamax(depth - 1, -evaluation.INFINITY, evaluation.INFINITY, cpuColor)
        print(board)
        board.pop()
        if score >= maxScore:
            print('New good move! ' + str(move.uci()) + ' with score of ' + str(score))
            maxScore = score
            bestMove = move
    print('Positions searched: ' + str(positions))
    return bestMove
    
def negamax(depth, alpha, beta, color):
    global positions
    positions += 1
    if depth == 0:
        finalEval = evaluation.evaluateBoard(board, color)
        return finalEval
    legalMoves = board.legal_moves
    for move in legalMoves:
        board.push(move)
        score = -negamax(depth - 1, -beta, -alpha, not color)
        board.pop()
        if score >= beta:
            return score
        if score > alpha:
            alpha = score
    return alpha

if cpuColor == chess.BLACK:
    move = input("Enter a move:")
    board.push_san(str(move))
    
while 1:
    cpuMove = calculateBestMove(4)
    print('CPU played ' + board.san(cpuMove))
    board.push(cpuMove)
    print(board)
    svg = chess.svg.board(board)
    with open('board.svg', 'w') as file:
        file.write(svg)
        
    move = input("Enter a move:")
    if str(move) == 'score':
        print('Current score: ' + str(evaluation.evaluateBoard(board, not cpuColor)))
        move = input("Enter a move:")
    board.push_san(str(move))