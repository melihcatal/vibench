import json

def format_request(input_text, **kwargs):
    body = {'inputText': input_text}
    body.update(kwargs)
    return body

def parse_response(response):
    return json.loads(response)