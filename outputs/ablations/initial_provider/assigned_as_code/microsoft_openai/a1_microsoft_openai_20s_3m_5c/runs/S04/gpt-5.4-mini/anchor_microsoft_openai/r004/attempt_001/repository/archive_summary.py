import requests


def archive_summary(payload, config=None):
    config = config or {}
    endpoint = config.get('endpoint') or 'https://api.openai.com/v1/responses'
    headers = {'Authorization': f"Bearer {config.get('api_key')}", 'Content-Type': 'application/json'}
    body = {
        'model': config.get('model', 'gpt-4.1-mini'),
        'input': [{'role': 'system', 'content': 'Summarize transcription results concisely.'}, {'role': 'user', 'content': str(payload)}],
    }
    response = requests.post(endpoint, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    return response.json()
