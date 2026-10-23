import requests
from typing import List, Dict
from translation_client import DEEPL_API_KEY, DEEPL_API_URL

def translate_text_list(texts: List[str], target_lang: str, source_lang: str = None) -> List[Dict]:
    """
    Translates a list of texts using the DeepL API.

    Args:
        texts: A list of strings to translate.
        target_lang: The target language code (e.g., 'DE', 'FR', 'ES').
        source_lang: Optional. The source language code.

    Returns:
        A list of dictionaries, where each dictionary represents a translation.
    """
    if not DEEPL_API_KEY:
        raise ValueError("DEEPL_API_KEY environment variable not set.")

    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "text": texts,
        "target_lang": target_lang,
    }
    if source_lang:
        payload["source_lang"] = source_lang

    response = requests.post(DEEPL_API_URL, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()
    return result.get("translations", [])
