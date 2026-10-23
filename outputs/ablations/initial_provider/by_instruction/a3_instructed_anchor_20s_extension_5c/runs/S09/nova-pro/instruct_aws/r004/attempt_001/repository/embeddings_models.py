import json

def create_request(text: str):
    return json.dumps({'inputs': text})

def parse_response(response):
    return json.loads(response)['embedding']