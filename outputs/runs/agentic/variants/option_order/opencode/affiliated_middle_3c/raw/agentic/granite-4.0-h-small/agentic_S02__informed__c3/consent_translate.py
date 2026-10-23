import os
import json
from typing import Dict, Any

from Model.identity_models import UserProfile

# Provider: DeepL API (document translation)
DEEPL_TRANSLATE_URL = "https://api.deepl.com/v2/translate"


def translate_consent(
    consent_text: str,
    target_lang: str = "es",
    api_key: str = os.getenv("DEEPL_AUTH_KEY"),
) -> str:
    """Translate identity‑provider consent copy to the requested language.

    Args:
        consent_text: Original consent copy (usually HTML or plain text).
        target_lang: ISO‑639‑1 language code (e.g., 'es', 'fr').
        api_key: DeepL API authentication key.

    Returns:
        Translated consent text.
    """
    payload = {
        "text": consent_text,
        "target_lang": target_lang.upper(),
    }
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    with IdentityClient.ImmutableHttpClient(DEEPL_TRANSLATE_URL) as http:
        http.request("POST", payload=payload, headers=headers)
        resp = http.getresponse()
        resp_body = resp.read().decode()
        result = json.loads(resp_body)
    return result["translations"][0]["text"]
