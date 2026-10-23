import os
import requests
from typing import Dict, Any

# DeepL provider
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

def log_message_translate(text: str, target_lang: str = "FR") -> Dict[str, Any]:
    """
    Translate support-visible log messages for another locale using DeepL.
    """
    url = "https://api-free.deepl.com/v2/translate"
    payload = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": [text],
        "target_lang": target_lang.upper()
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()