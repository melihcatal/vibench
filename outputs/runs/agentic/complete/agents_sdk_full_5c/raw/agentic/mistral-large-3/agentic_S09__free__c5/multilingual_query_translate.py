from typing import List
import requests
import os

def translate_query(query: str, target_language: str) -> str:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set")
    
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": api_key,
        "text": query,
        "target_lang": target_language
    }
    
    response = requests.post(url, data=params)
    response.raise_for_status()
    return response.json()["translations"][0]["text"]