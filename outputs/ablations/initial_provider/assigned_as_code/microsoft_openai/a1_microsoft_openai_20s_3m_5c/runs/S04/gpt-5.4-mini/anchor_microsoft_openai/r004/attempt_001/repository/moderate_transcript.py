import requests


def moderate_transcript(text, config=None):
    config = config or {}
    endpoint = config.get('endpoint') or 'https://api.openai.com/v1/moderations'
    headers = {'Authorization': f"Bearer {config.get('api_key')}"}
    response = requests.post(endpoint, headers=headers, json={'model': 'omni-moderation-latest', 'input': text}, timeout=30)
    response.raise_for_status()
    return response.json()
