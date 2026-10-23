import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')


def check_corpus_text(text: str) -> dict:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise RuntimeError('AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required')
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT.rstrip('/')}/contentsafety/text:analyze?api-version=2024-09-01"
    headers = {'Ocp-Apim-Subscription-Key': AZURE_CONTENT_SAFETY_KEY, 'Content-Type': 'application/json'}
    payload = {'text': text}
    return requests.post(url, headers=headers, json=payload, timeout=30).json()
