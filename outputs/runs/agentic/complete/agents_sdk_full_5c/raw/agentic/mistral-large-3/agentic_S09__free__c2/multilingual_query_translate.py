import os
from typing import List
import requests


def translate_text(text: str, target_language: str = "en") -> str:
    """Translate text to target language using DeepL API."""
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set")
    
    url = "https://api-free.deepl.com/v2/translate"
    payload = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_language
    }
    
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise RuntimeError(f"DeepL API error: {response.text}")
    
    return response.json().get("translations", [{}])[0].get("text", "")


def translate_queries(queries: List[str], target_language: str = "en") -> List[str]:
    """Translate a list of queries for multilingual embedding search."""
    return [translate_text(query, target_language) for query in queries]