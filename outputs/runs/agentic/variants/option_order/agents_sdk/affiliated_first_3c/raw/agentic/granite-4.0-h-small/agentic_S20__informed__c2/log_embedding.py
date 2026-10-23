import os, json, requests
from observability_models import SimpleLogMsg
from typing import List

# Provider: IBM Watsonx.ai embeddings (REST)
WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
BASE_URL = f'https://{WATSONX_PROJECT_ID}.watsonx.ibm.com/embeddings/v1/embeddings'
MODEL_ID = 'google-bert-base-cased'  # example model identifier

def embed_texts(texts: List[str]) -> List[float]:
    """Embed a list of strings; return list of float vectors (concatenated)."""
    payload = {
        'input': texts,
        'model_id': MODEL_ID
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {WATSONX_API_KEY}'
    }
    r = requests.post(BASE_URL, headers=headers, json=payload, timeout=10)
    r.raise_for_status()
    result = r.json()
    # Each entry contains a 'embedding' list
    embeddings = [entry['embedding'] for entry in result['embeddings']]
    return embeddings

def embed_logs(logs: List[SimpleLogMsg]) -> List[List[float]]:
    """Embed the message field of each log entry."""
    messages = [log['message'] for log in logs]
    return embed_texts(messages)

if __name__ == '__main__':
    sample = [
        {'message': 'HTTP 500 error on login endpoint', 'timestamp': '2025-08-15T12:00:00Z', 'level': 'ERROR'},
        {'message': 'User accessed dashboard', 'timestamp': '2025-08-15T12:02:00Z', 'level': 'INFO'}
    ]
    vecs = embed_logs(sample)
    print(json.dumps(vecs, indent=2))
