from utils import read_text, read_json, piecemap
from langchain.prompts import (
    FewShotChatMessagePromptTemplate
)
from langchain.prompts.chat import (
    ChatPromptTemplate,
)
from chat import get_response
from test import run_tests
import chess

class Simple:
    def __init__(self, system_template_path, human_template_path):
        self.system_template = read_text(system_template_path)
        self.human_template = read_text(human_template_path)

    def get_human_prompt(self, fen):
        return fen 

    def parse_output(self, response):
        return response

    def __call__(self, fen):
        chat_template = ChatPromptTemplate.from_messages([
            ("system", self.system_template),
            ("human", self.get_human_prompt(fen))
        ])
        formatted_prompt = chat_template.format_messages(input=fen)

        response = get_response(formatted_prompt, model="gpt-3.5-turbo", temp=0)

        output = self.parse_output(response)
        return output

class SimpleFewShot:
    def __init__(self, system_template_path, human_template_path):
        self.system_template = read_text(system_template_path)
        self.human_template = read_text(human_template_path)

    def get_system_prompt(self):
        return read_text()

    def get_human_prompt(self, fen):
        return fen

    def parse_output(self, output):
        return output
    
    def get_few_shot_examples(self):
        examples = []
        data = read_json("dataset_few_shot.json")
        for puzzle in data[:15]:
            fen = puzzle["puzzle_data"]["puzzle_fen"]
            input_prompt = self.get_human_prompt(fen) 

            lines = puzzle["puzzle_data"]["lines"]
            for key in lines:
                if lines[key] != "retry":
                    correct_move = key
            output_prompt = correct_move
            examples.append({
                "input": input_prompt,
                "output": output_prompt
            })


        example_template = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"),
                ("ai", "{output}")
            ]
        )

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_template,
            examples=examples
        )
        return few_shot_prompt
    
    def __call__(self, fen):
        chat_template = ChatPromptTemplate.from_messages([
            ("system", self.system_template),
            self.get_few_shot_examples(),
            ("human", self.get_human_prompt(fen))
        ])
        formatted_prompt = chat_template.format_messages(input=fen)

        response = get_response(formatted_prompt, model="gpt-3.5-turbo", temp=0)

        output = self.parse_output(response)
        return output

class Baseline(Simple):
    """
    Simplest one. Board format is given in raw FEN. No chain of thought. Achieves 2% accuracy.
    """
    def __init__(self):
        super().__init__("templates/baseline/system.txt", "templates/baseline/human.txt")

class BaselineFewShot(SimpleFewShot):
    """
    Simplest one, with raw fen as input, with 50 few shot examples. 
    """
    def __init__(self):
        super().__init__("templates/baseline/system.txt", "templates/baseline/human.txt")

class LanguageBoardRepr(SimpleFewShot):
    def __init__(self):
        path = "templates/languageboardrepr/"
        super().__init__(path+"system.txt",path+"human.txt")
    
    def get_human_prompt(self, fen):
        s = ""
        board = chess.Board(fen)
        square_to_piece, piece_to_square = piecemap(board)
        for piece in piece_to_square:
            if piece == "P":
                if len(piece_to_square[piece] > 1):
                    s += "There are black pawns on "
                s += "There are "


class BaselineAscii(Simple):
    """
    Simple ascii board (no row-col notation), color to move
    """
    def __init__(self):
        super().__init__("templates/baseline2/system.txt", "templates/baseline2/human.txt")
    
    def get_human_prompt(self, fen):
        board = chess.Board(fen)

        if board.turn == True:
            color = "White"
        else:
            color = "Black"
        
        board_repr = str(board)
        
        prompt = self.human_template.format(color=color, board=board_repr)
        return prompt

class BaselineImproved(Simple):
    """
    each square with each piece, color to move
    """
    def __init__(self):
        path = "templates/baseline3/"
        super().__init__(path+"system.txt", path+"human.txt")
    
    def get_human_prompt(self, fen):
        square_to_piece = ""

        board = chess.Board(fen)
        if board.turn == True:
            color = "White"
        else:
            color = "Black"

        squares = []
        for letter in ["a","b","c","d","e","f","g","h"]:
            for number in range(1,9):
                squares.append(letter + str(number))
        for square in squares:
            piece = board.piece_at(chess.parse_square(square))
            square_to_piece += f"{square} {piece}\n"

        prompt = self.human_template.format(pieces=square_to_piece, color=color)
        return prompt

run_tests(BaselineFewShot())