import json

def read_text(path):
    with open(path) as f:
        s = f.read()
    return s

def read_json(path):
    with open(path) as f:
        data = json.load(f)
    return data