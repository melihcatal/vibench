import json

def prepare_payload(text, max_tokens=4096, temperature=0, top_p=0.9):
    return {
        'inputText': text,
        'textGenerationConfig': {
            'maxTokenCount': max_tokens,
            'temperature': temperature,
            'topP': top_p
        }
    }

def parse_response(response):
    return response.get('results')[0].get('outputText')