from typing import List, Dict, Any
import requests
import os


def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates text to a target language using DeepL API.

    Args:
        text: Input text to translate.
        target_language: Target language code. Defaults to "en" (English).

    Returns:
        str: Translated text.

    Raises:
        ValueError: If the DEEPL_API_KEY environment variable is not set.
    """
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")

    url = "https://api-free.deepl.com/v2/translate"
    payload = {"auth_key": api_key, "text": text, "target_lang": target_language}

    response = requests.post(url, data=payload)
    response.raise_for_status()

    return response.json()["translations"][0]["text"]


def translate_queries(queries: List[str], target_language: str = "en") -> List[str]:
    """
    Translates a list of queries for multilingual embedding search using DeepL API.

    Args:
        queries: List of input queries to translate.
        target_language: Target language code. Defaults to "en" (English).

    Returns:
        List[str]: List of translated queries.
    """
    return [translate_text(query, target_language) for query in queries]
