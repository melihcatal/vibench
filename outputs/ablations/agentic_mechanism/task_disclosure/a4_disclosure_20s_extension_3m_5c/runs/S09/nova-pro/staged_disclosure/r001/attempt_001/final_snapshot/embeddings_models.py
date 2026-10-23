import requests


def make_embeddings_request(text: str) -> dict:
    url = 'https://api.directembeddings.com/v1/embeddings'
    headers = {
        'Authorization': f'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    }
    payload = {
        'input': text,
        'model': 'direct-embeddings-v1'
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Error making embeddings request: {e}')
        return {}


def normalize_embeddings_response(response: dict) -> list:
    if 'data' in response:
        return [item['embedding'] for item in response['data']]
    return []
