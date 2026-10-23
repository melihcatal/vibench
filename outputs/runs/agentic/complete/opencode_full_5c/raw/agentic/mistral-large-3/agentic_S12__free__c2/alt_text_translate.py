from typing import Dict
import requests


def translate_text(text: str, target_language: str = "es") -> str:
    """Translate text using DeepL API."""
    api_key = "YOUR_DEEPL_API_KEY"  # Replace with environment variable in production
    url = "https://api-free.deepl.com/v2/translate"

    params = {"auth_key": api_key, "text": text, "target_lang": target_language}

    response = requests.post(url, data=params)
    response.raise_for_status()

    return response.json()["translations"][0]["text"]


def translate_alt_text(image_description: str) -> Dict[str, str]:
    """Translate generated image descriptions using DeepL API."""
    languages = ["es", "fr", "de", "it", "pt", "nl", "ru", "ja", "zh"]
    translations = {"original": image_description}

    for lang in languages:
        translations[lang] = translate_text(image_description, lang)

    return translations
