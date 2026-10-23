import os
from typing import List, Dict
import requests

def translate_transcript(segments: List[Dict[str, str]], target_language: str = "es") -> List[Dict[str, str]]:
    """
    Translates transcript segments using DeepL API.
    Returns translated segments with original metadata.
    """
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/json"
    }
    
    texts = [segment["text"] for segment in segments]
    data = {
        "text": texts,
        "target_lang": target_language
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    translations = response.json()["translations"]
    
    return [{
        **segments[i],
        "translated_text": translations[i]["text"]
    } for i in range(len(segments))]