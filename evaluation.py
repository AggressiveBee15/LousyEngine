import chess
import math

INFINITY = 1000000

# Useful links: https://github.com/stannous/shatranj/blob/master/shatranj.py#L1912

def reverseList(orderedList):
    return list(reversed(orderedList))

pawnEvalWhite =[
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

pawnEvalBlack = reverseList(pawnEvalWhite)

knightEval = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

bishopEvalWhite = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

bishopEvalBlack = reverseList(bishopEvalWhite)

rookEvalWhite = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

rookEvalBlack = reverseList(rookEvalWhite)

evalQueen = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

kingEvalWhite = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]
kingEvalBlack = reverseList(kingEvalWhite)

# Link: http://chessprogramming.wikispaces.com/Simplified+evaluation+function
pieceValues = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def getPieceSquareScore(pieceObj, x, y):
    pieceSymbol = pieceObj.symbol().lower()
    isWhite = pieceObj.color
    if pieceSymbol == 'p':
        return (pawnEvalWhite[y][x] if isWhite else pawnEvalBlack[y][x])
    elif pieceSymbol == 'r':
      return (rookEvalWhite[y][x] if isWhite else rookEvalBlack[y][x])
    elif pieceSymbol == 'n':
      return knightEval[y][x]
    elif pieceSymbol == 'b':
      return (bishopEvalWhite[y][x] if isWhite else bishopEvalBlack[y][x])
    elif pieceSymbol == 'q':
        return evalQueen[y][x]
    elif pieceSymbol == 'k':
        return (kingEvalWhite[y][x] if isWhite else kingEvalBlack[y][x])

def getPieceCount(board, piece, color):
    return len(board.pieces(piece, color))

def calculatePieceSquareScore(board):
    whiteScore = 0
    blackScore = 0
    for color in chess.COLORS:
        for pieceType in chess.PIECE_TYPES:
            squares = board.pieces(pieceType, color)
            for square in squares:
                x = chess.square_file(square)
                y = chess.square_rank(square)
                
                piece = board.piece_at(square)
                if color == chess.WHITE:
                    whiteScore += getPieceSquareScore(piece, x, y)
                else:
                    blackScore += getPieceSquareScore(piece, x, y)
    return whiteScore - blackScore

def evaluateBoard(board, sideToMove):
    evaluationScore = 0
    multiplier = (1 if sideToMove == chess.WHITE else -1)
    if board.is_checkmate():
        print('Checkmate detected')
        return INFINITY * multiplier
    # 1. Evaluate piece count first
    evaluationScore += (pieceValues[chess.KING] * (getPieceCount(board, chess.KING, chess.WHITE) - getPieceCount(board, chess.KING, chess.BLACK))
            + pieceValues[chess.QUEEN] * (getPieceCount(board, chess.QUEEN, chess.WHITE) - getPieceCount(board, chess.QUEEN, chess.BLACK))
            + pieceValues[chess.ROOK] * (getPieceCount(board, chess.ROOK, chess.WHITE) - getPieceCount(board, chess.ROOK, chess.BLACK))
            + pieceValues[chess.KNIGHT] * (getPieceCount(board, chess.KNIGHT, chess.WHITE) - getPieceCount(board, chess.KNIGHT, chess.BLACK))
            + pieceValues[chess.BISHOP] * (getPieceCount(board, chess.BISHOP, chess.WHITE) - getPieceCount(board, chess.BISHOP, chess.BLACK))
            + pieceValues[chess.PAWN] * (getPieceCount(board, chess.PAWN, chess.WHITE) - getPieceCount(board, chess.PAWN, chess.BLACK)))
    return evaluationScore * multiplier