import os
import requests
from typing import Optional
from model_models import TranslationRequest, TranslationResponse


def translate_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> TranslationResponse:
    """Translate generated model output using DeepL API."""
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")

    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/json",
    }

    payload = {"text": [text], "target_lang": target_language.upper()}

    if source_language:
        payload["source_lang"] = source_language.upper()

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        translations = result.get("translations", [])
        if not translations:
            raise Exception("No translation returned")

        translation = translations[0]

        return TranslationResponse(
            translated_text=translation.get("text", ""),
            source_language=translation.get(
                "detected_source_language", source_language or "unknown"
            ).lower(),
            target_language=target_language.lower(),
            provider="deepl",
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to translate text: {str(e)}")
