import json
import chess

def read_text(path):
    with open(path) as f:
        s = f.read()
    return s

def read_json(path):
    with open(path) as f:
        data = json.load(f)
    return data

def piecemap(board):
    squares = []
    for letter in ["a","b","c","d","e","f","g","h"]:
        for number in range(1,9):
            squares.append(letter + str(number))

    square_to_piece = {}
    piece_to_square = {}
    for square in squares:
        piece = board.piece_at(chess.parse_square(square))
        if piece in piece_to_square:
            piece_to_square[piece].append(square)
        else:
            piece_to_square[piece] = [square]
        if square in square_to_piece:
            square_to_piece[square] = piece

    return (square_to_piece, piece_to_square)