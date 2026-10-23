def normalize_request(prompt):
    return {'inputText': prompt, 'textGenerationConfig': {'maxTokenCount': 512}}

def parse_response(response):
    return response['outputText']