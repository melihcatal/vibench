import json

def normalize_embedding_response(response):
    result = json.loads(response['body'].read())
    return result['embedding']