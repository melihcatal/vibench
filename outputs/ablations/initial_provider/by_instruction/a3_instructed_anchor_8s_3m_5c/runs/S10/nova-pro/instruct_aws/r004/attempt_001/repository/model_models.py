import json

def create_request(text, max_tokens=512, temperature=0.5, top_p=0.9):
    return {
        'inputText': text,
        'textGenerationConfig': {
            'maxTokenCount': max_tokens,
            'temperature': temperature,
            'topP': top_p
        }
    }

def parse_response(response):
    return response['results'][0]['outputText']