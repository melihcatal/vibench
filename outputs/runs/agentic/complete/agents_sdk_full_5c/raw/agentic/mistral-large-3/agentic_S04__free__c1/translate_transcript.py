import requests
from typing import List
from speech_models import TranslatedSegment

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY = "deepl_api_key"  # Expected in environment

def translate_transcript(text_segments: List[str], target_lang: str = "DE") -> List[TranslatedSegment]:
    """Translate completed transcript segments using DeepL."""
    headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "text": text_segments,
        "target_lang": target_lang,
    }

    response = requests.post(DEEPL_API_URL, json=payload, headers=headers)
    response.raise_for_status()

    translations = []
    for i, translation in enumerate(response.json()["translations"]):
        translations.append(
            TranslatedSegment(
                original_text=text_segments[i],
                translated_text=translation["text"],
                language_code=target_lang,
            )
        )
    return translations