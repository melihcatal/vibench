from typing import List
import requests
import os


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set")

    url = "https://api-free.deepl.com/v2/translate"
    payload = {"auth_key": api_key, "text": query, "target_lang": target_language}

    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise ValueError(f"DeepL API request failed: {response.text}")

    result = response.json()
    return result.get("translations", [{}])[0].get("text", query)
