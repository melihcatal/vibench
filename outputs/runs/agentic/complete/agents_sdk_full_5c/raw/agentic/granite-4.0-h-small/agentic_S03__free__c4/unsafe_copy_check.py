import os
import requests
from translation_client import TranslationClient

def scan_unsafe_localized_copy(texts: List[str]) -> List[bool]:
    """Check localized (translated) copy for unsafe content using Azure Content Safety.
    Provider: Azure Content Safety (identified by env vars AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY).
    """
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    if not endpoint or not key:
        raise RuntimeError('Missing Content Safety environment variables')
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }
    # Simple moderation request: returns a flag indicating safe/unsafe
    payload = {
        'texts': texts,
        'model': 'default'  # hypothetical model ID
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    # Assume result format: {'results': [{'isSafe': True}, ...]}
    return [item['isSafe'] for item in result.get('results', [])]

if __name__ == '__main__':
    sample = ['Hello', 'Buy now!', 'Visit http://bad.example.com']
    safe_flags = scan_unsafe_localized_copy(sample)
    for txt, safe in zip(sample, safe_flags):
        print(f'{txt}: {'SAFE' if safe else 'UNSAFE'}')