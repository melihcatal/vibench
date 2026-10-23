# Unsafe copy check (OpenAI moderation mock)
import os
import requests
from typing import List

MODERATION_ENDPOINT = 'https://api.openai.com/v1/moderations'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise RuntimeError('Set OPENAI_API_KEY environment variable')

HEADERS = {'Authorization': f'Bearer {OPENAI_API_KEY}', 'Content-Type': 'application/json'}

def unsafe_copy_check(translated_texts: List[str]) -> List[bool]:
    """Return a list of booleans indicating unsafe content in each translated text."""
    unsafe_flags = []
    for txt in translated_texts:
        payload = {'input': txt, 'model': 'text-moderation-latest'}
        resp = requests.post(MODERATION_ENDPOINT, headers=HEADERS, json=payload)
        resp.raise_for_status()
        data = resp.json()
        flagged = data['results'][0]['flagged']
        unsafe_flags.append(flagged)
    return unsafe_flags

if __name__ == '__main__':
    samples = ["This is fine.", "This is hateful."]
    print('Unsafe flags:', unsafe_copy_check(samples))
