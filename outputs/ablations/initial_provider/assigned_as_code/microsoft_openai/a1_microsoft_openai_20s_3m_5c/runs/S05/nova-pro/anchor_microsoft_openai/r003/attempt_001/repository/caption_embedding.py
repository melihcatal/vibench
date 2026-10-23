import requests

def embed_caption(caption):
    url = f'https://api.sentence-transformers.com/v1/embeddings?api_key={os.getenv('SENTENCE_TRANSFORMERS_API_KEY')}'
    data = {
        'sentences': [caption]
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()['data'][0]['embedding']