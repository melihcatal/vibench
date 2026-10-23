import requests

DIRECT_EMBEDDINGS_API_URL = 'https://api.directembeddings.com/v1/embeddings'

def create_embedding_request(text: str) -> dict:
    return {
        'input': text,
        'model': 'direct-embeddings-v1'
    }

def send_embedding_request(request: dict) -> dict:
    response = requests.post(DIRECT_EMBEDDINGS_API_URL, json=request)
    return response.json()

def normalize_embedding_response(response: dict) -> list:
    if 'data' in response:
        return [item['embedding'] for item in response['data']]
    return []