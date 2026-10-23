import json
import os
import requests
from database_models import normalize_document

def translate_text(text, target_lang, api_key):
    """Translate text using Google Cloud Translation API."""
    endpoint = os.getenv("GOOGLE_TRANSLATE_ENDPOINT") or "https://translation.googleapis.com/v3/projects/translate/text:translate"
    params = {
        "targetLanguageCode": target_lang,
        "sourceLanguageCode": "en"
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"contents": [text]}
    response = requests.post(endpoint, headers=headers, params=params, json=payload)
    response.raise_for_status()
    result = response.json()
    translated = result["translatedText"]
    return translated

if __name__ == "__main__":
    translated = translate_text("Hello, how are you?", "es", os.getenv("GOOGLE_API_KEY"))
    print("Translation:", translated)
