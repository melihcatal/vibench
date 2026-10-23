import os
import requests


def ocr_safety(payload, config=None):
    config = config or {}
    endpoint = config.get('endpoint') or os.environ['PERSPECTIVE_API_ENDPOINT']
    key = config.get('api_key') or os.environ['PERSPECTIVE_API_KEY']
    headers = {'Content-Type': 'application/json', 'X-Goog-Api-Key': key}
    body = {'comment': {'text': payload['text']}, 'languages': config.get('languages', ['en'])}
    response = requests.post(endpoint, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    return {'safety': response.json()}
