import requests
from typing import Dict, Any
from security_client import get_secrets_config

def translate_runbook_notes(text: str, target_lang: str = "EN") -> str:
    config = get_secrets_config()
    api_key = config['deepl_api_key']
    if not api_key:
        raise ValueError("DEEPL_API_KEY not set")
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(url, data=params)
    response.raise_for_status()
    return response.json()["translations"][0]["text"]