def normalize_request(input_text):
    return {'prompt': input_text,'max_tokens': 150}

def parse_response(response):
    return response['choices'][0]['text'].strip()