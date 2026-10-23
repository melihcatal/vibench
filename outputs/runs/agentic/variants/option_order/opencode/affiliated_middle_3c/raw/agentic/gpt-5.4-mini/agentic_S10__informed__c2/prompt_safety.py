import os
import requests
from model_models import normalize_text, safety_result


def check_prompt_safety(text: str) -> dict:
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT', '').rstrip('/')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY', '')
    if not endpoint or not key:
        return safety_result(False, 'Azure AI Content Safety not configured')
    payload = {'text': normalize_text(text)}
    resp = requests.post(
        f'{endpoint}/contentsafety/text:analyze?api-version=2024-09-01',
        headers={'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/json'},
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return safety_result(True, data)
