import os, json, requests

# IBM Watsonx Slate embeddings endpoint (hosted service)
EMBED_URL = 'https://api.watsonx.ibm.com/v1/embeddings'
API_KEY = os.getenv('WATSONX_API_KEY')
PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')


def embed_message(message: str) -> list:
    """Generate a vector embedding for a log message using Watsonx Slate embeddings.",
    Returns a list of floats representing the embedding vector.
    """
    payload = {
        'inputs': [message]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    resp = requests.post(EMBED_URL, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # Expected format: {'embeddings': [{'embedding': [0.1, 0.2, ...]}]}
    try:
        return data['embeddings'][0]['embedding']
    except (KeyError, IndexError):
        return []

# Example usage (commented for CI)
# if __name__ == '__main__':
#     vec = embed_message('Server timeout on GET /api/users')
#     print('Embedding vector length:', len(vec))
