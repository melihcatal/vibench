import os
import requests


def transcript_embedding(text):
    response = requests.post(
        'https://api.embed.com/v1/embed',
        params={'api_key': os.environ['EMBED_API_KEY'], 'text': text},
        timeout=30
    )
    response.raise_for_status()
    return response.json()['embedding']