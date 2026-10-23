import os
from typing import List, Optional
import requests

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_queries(
    queries: List[str],
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> List[str]:
    key = auth_key or DEEPL_AUTH_KEY
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    data = {
        "text": queries,
        "target_lang": target_lang,
    }
    if source_lang:
        data["source_lang"] = source_lang
    headers = {
        "Authorization": f"DeepL-Auth-Key {key}",
    }
    response = requests.post(DEEPL_API_URL, data=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    return [t["text"] for t in result["translations"]]


def translate_and_embed_prepare(
    queries: List[str],
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> List[dict]:
    translated = translate_queries(queries, target_lang, source_lang, auth_key)
    return [
        {"original": original, "translated": translated[i]}
        for i, original in enumerate(queries)
    ]


def detect_and_translate(
    query: str,
    target_lang: str = "EN",
    auth_key: Optional[str] = None,
) -> dict:
    key = auth_key or DEEPL_AUTH_KEY
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    data = {
        "text": [query],
        "target_lang": target_lang,
    }
    headers = {
        "Authorization": f"DeepL-Auth-Key {key}",
    }
    response = requests.post(DEEPL_API_URL, data=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    translation = result["translations"][0]
    return {
        "original": query,
        "translated": translation["text"],
        "detected_source": translation.get("detected_source_language", "unknown"),
        "target_lang": target_lang,
    }
