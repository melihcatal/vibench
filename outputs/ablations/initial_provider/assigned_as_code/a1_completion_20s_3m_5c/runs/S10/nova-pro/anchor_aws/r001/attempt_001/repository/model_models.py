import json

def normalize_response(response):
    return response.get('completions')[0].get('data').get('text')