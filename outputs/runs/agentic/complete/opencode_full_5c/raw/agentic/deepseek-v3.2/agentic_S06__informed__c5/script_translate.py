import os
import requests
from typing import List, Dict, Optional


def translate_text(
    text: str, target_language: str = "en", source_language: str = "auto"
) -> str:
    """
    Translate narration scripts before synthesis using DeepL API.
    """
    api_key = os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    url = "https://api-free.deepl.com/v2/translate"

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "text": [text],
        "target_lang": target_language.upper(),
        "source_lang": source_language.upper() if source_language != "auto" else None,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        translations = result.get("translations", [])

        if translations:
            return translations[0].get("text", text)
        else:
            return text

    except requests.exceptions.RequestException as e:
        raise Exception(f"Translation failed: {str(e)}")


def translate_batch(
    texts: List[str], target_language: str = "en", source_language: str = "auto"
) -> List[str]:
    """
    Translate multiple narration scripts in batch.
    """
    api_key = os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    url = "https://api-free.deepl.com/v2/translate"

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "text": texts,
        "target_lang": target_language.upper(),
        "source_lang": source_language.upper() if source_language != "auto" else None,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        translations = result.get("translations", [])

        return [t.get("text", texts[i]) for i, t in enumerate(translations)]

    except requests.exceptions.RequestException as e:
        raise Exception(f"Batch translation failed: {str(e)}")
