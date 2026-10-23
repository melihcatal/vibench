def normalize_request(input_text):
    return {
        'inputText': input_text
    }

def parse_response(response_body):
    return response_body.decode('utf-8')