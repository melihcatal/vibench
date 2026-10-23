from typing import Dict, Any
import requests
from messaging_models import EventResponse

DEEPL_API_KEY = "...")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

def translate_payload(message: EventResponse, target_lang: str = "EN") -> str:
    text = str(message.payload.get("text", ""))
    if not text:
        return ""
    
    payload = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(DEEPL_API_URL, data=payload)
    response.raise_for_status()
    
    return response.json()["translations"][0]["text"]