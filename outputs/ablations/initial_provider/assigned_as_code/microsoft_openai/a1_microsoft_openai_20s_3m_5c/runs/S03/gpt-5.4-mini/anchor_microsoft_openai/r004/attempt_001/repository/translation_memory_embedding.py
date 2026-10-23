import requests

from translation_client import load_translation_config


def translation_memory_embedding(payload, config=None):
    config = load_translation_config(config)
    response = requests.post(
        'https://api.openai.com/v1/embeddings',
        headers={'Authorization': 'Bearer ' + config['api_key'], 'Content-Type': 'application/json'},
        json={'model': 'text-embedding-3-small', 'input': payload['text']},
        timeout=config['timeout'],
    )
    response.raise_for_status()
    data = response.json()
    return {'embedding': data['data'][0]['embedding'], 'text': payload['text']}
