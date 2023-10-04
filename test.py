from chat import get_response, get_batch_response
from utils import read_json

def run_tests(program):
    dataset = read_json("dataset.json") 
    num_correct = 0
    for puzzle in dataset:
        fen = puzzle["puzzle_data"]["puzzle_fen"]
        correct_moves = puzzle["puzzle_data"]["lines"]
        rating = puzzle["metadata"]["rating"]

        move = program(fen)

        if move in correct_moves and correct_moves[move] != "retry":
            correct = True
            num_correct += 1
        else:
            correct = False

        print(f"{rating:4} {move:6} {correct}")        
    
    print("total correct", num_correct)
    print("tests complete") 

######################