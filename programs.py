from utils import read_text
from langchain.prompts.chat import (
    ChatPromptTemplate
)
from chat import get_response
from test import run_tests

class Simple:
    def __init__(self, system_template_path, human_template_path):
        self.system_template = read_text(system_template_path)
        self.human_template = read_text(human_template_path)

    def fen_to_repr(self, fen):
        return fen 

    def response_to_uci(self, response):
        return response

    def __call__(self, fen):
        chat_template = ChatPromptTemplate.from_messages([
            ("system", self.system_template),
            ("human", self.human_template)
        ])
        formatted_prompt = chat_template.format_messages(input=fen)

        response = get_response(formatted_prompt, model="gpt-3.5-turbo", temp=0)

        output = self.response_to_uci(response)
        return output

class SimpleFewShot:
    pass

class Baseline(Simple):
    def __init__(self):
        super().__init__("templates/baseline/system.txt", "templates/baseline/human.txt")

run_tests(Baseline())