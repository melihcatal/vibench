import os
import httpx
from safety_models import AppealTranslation

DEEPL_API_URL = "https://api.deepl.com/v2/translate"


def _get_deepl_api_key() -> str:
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")
    return api_key


def appeal_translate(
    text: str, target_language: str = "EN", source_language: str | None = None
) -> AppealTranslation:
    api_key = _get_deepl_api_key()
    params = {
        "text": text,
        "target_lang": target_language,
        "auth_key": api_key,
    }
    if source_language:
        params["source_lang"] = source_language
    response = httpx.post(DEEPL_API_URL, data=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    translated = data["translations"][0]["text"]
    detected_source = data["translations"][0].get(
        "detected_source_language", source_language or "UNKNOWN"
    )
    return AppealTranslation(
        original_text=text,
        translated_text=translated,
        source_language=detected_source,
        target_language=target_language,
    )
