from typing import Dict
import requests
from identity_models import ConsentTranslation

# DeepL API for translation with concrete model identifier
PROVIDER_NAME = "deepl"
API_ENDPOINT = "https://api-free.deepl.com/v2/translate"
MODEL_ID = "deepl-translator-v2"


def translate_consent_text(text: str, target_language: str) -> ConsentTranslation:
    """Translate identity-provider consent copy using DeepL API."""
    auth_key = "DEEPL_AUTH_KEY"
    if not auth_key:
        raise ValueError("DeepL authentication key not configured")

    headers = {
        "Authorization": f"DeepL-Auth-Key {auth_key}",
        "Content-Type": "application/json",
    }

    data = {"text": [text], "target_lang": target_language.upper()}

    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    translated_text = result.get("translations", [{}])[0].get("text", text)

    return ConsentTranslation(
        original_text=text,
        translated_text=translated_text,
        target_language=target_language,
        provider=PROVIDER_NAME,
        model_id=MODEL_ID,
    )
