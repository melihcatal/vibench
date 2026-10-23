import requests


def check_script_safety(text: str) -> dict:
    endpoint = __import__('os').getenv('AZURE_CONTENT_SAFETY_ENDPOINT', '').rstrip('/')
    key = __import__('os').getenv('AZURE_CONTENT_SAFETY_KEY', '')
    response = requests.post(f'{endpoint}/contentsafety/text:analyze?api-version=2024-09-01', headers={'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/json'}, json={'text': text}, timeout=60)
    response.raise_for_status()
    return response.json()
