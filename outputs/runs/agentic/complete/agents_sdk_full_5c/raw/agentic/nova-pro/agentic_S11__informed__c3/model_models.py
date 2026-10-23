def normalize_request(input_text):
    return {'inputText': input_text}

def parse_response(response):
    return response['outputText']