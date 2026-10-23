import os
import requests
import json
from identity_client import get_deepl_config


def translate_consent_text(text: str, target_lang: str = "en") -> str:
    config = get_deepl_config()
    if not config.auth_key:
        raise ValueError("DeepL authentication key not configured.")

    # DeepL Free API endpoint. Use api.deepl.com/v2/ for Pro
    api_url = "https://api-free.deepl.com/v2/translate"

    headers = {
        "Authorization": f"DeepL-Auth-Key {config.auth_key}",
        "Content-Type": "application/json",
    }

    data = {"text": [text], "target_lang": target_lang.upper()}

    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    result = response.json()

    if result and "translations" in result and len(result["translations"]) > 0:
        return result["translations"][0]["text"]
    return text
