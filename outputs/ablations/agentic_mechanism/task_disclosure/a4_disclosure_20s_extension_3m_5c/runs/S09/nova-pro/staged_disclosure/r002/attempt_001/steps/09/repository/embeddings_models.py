import requests

def make_embedding_request(text):
    url = 'https://api.directembeddings.com/v1/embed'
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    }
    payload = {
        'text': text
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def normalize_embedding(embedding):
    # Normalization logic here
    return embedding

def handle_embedding_response(response):
    if response.get('error'):
        raise Exception(response['error'])
    embedding = response.get('embedding')
    if embedding:
        return normalize_embedding(embedding)
    return None