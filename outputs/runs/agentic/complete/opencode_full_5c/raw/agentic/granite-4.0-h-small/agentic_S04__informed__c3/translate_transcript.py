import os
import requests
from speech_models import TranslationRequest, TranslationResponse
from typing import Any, Dict

# DeepL example (REST API)
DEEPL_API_KEY = os.getenv("DEEPL_AUTH_KEY")
DEEPL_ENDPOINT = "https://api.deepl.com/v2/translate"


def translate_transcript(
    input_text: str, source_lang: str = "en", target_lang: str = "es"
) -> str:
    """Translate a transcript (or segment) using DeepL API.

    Args:
        input_text (str): Source text to translate.
        source_lang (str): ISO language code of the source.
        target_lang (str): ISO language code of the target.

    Returns:
        str: Translated text.
    """
    if not DEEPL_API_KEY:
        raise RuntimeError(
            "DeepL API key not set. Define DEEPL_AUTH_KEY environment variable."
        )
    payload = {
        "auth_key": DEEPL_API_KEY,
        "text": input_text,
        "source_lang": source_lang.upper(),
        "target_lang": target_lang.upper(),
    }
    try:
        response = requests.post(DEEPL_ENDPOINT, data=payload)
        response.raise_for_status()
        result = response.json()
        # DeepL returns translations under "translations" list
        translated = result["translations"][0]["text"]
        return translated
    except requests.RequestException as exc:
        raise RuntimeError(f"DeepL translation failed: {exc}")


# Example wrapper that consumes our model objects
def translate_using_model(request: TranslationRequest) -> TranslationResponse:
    raw = translate_transcript(
        request.text, source_lang=request.source_lang, target_lang=request.target_lang
    )
    return TranslationResponse(translated_text=raw)
