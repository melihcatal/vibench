import os
from typing import Optional
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    normalize_language_code,
    normalize_text,
)
from translation_client import (
    GoogleTranslationClient,
    GOOGLE_TRANSLATE_API_KEY,
    GOOGLE_TRANSLATE_API_ENDPOINT,
    DEFAULT_GOOGLE_MODEL,
    create_translation_client,
)


def translate_text(
    text: str,
    source_language: str,
    target_language: str,
    model: str = DEFAULT_GOOGLE_MODEL,
    api_key: Optional[str] = None,
) -> TranslationResponse:
    key = api_key or GOOGLE_TRANSLATE_API_KEY
    client = create_translation_client(api_key=key)
    cleaned_text = normalize_text(text)
    request = TranslationRequest(
        text=cleaned_text,
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language),
        model=model,
        content_type="text",
    )
    return client.translate(request)


def translate_text_via_http(
    text: str,
    source_language: str,
    target_language: str,
    model: str = DEFAULT_GOOGLE_MODEL,
    api_key: Optional[str] = None,
) -> TranslationResponse:
    import requests

    key = api_key or os.environ.get("GOOGLE_TRANSLATE_API_KEY", "")
    endpoint = GOOGLE_TRANSLATE_API_ENDPOINT
    payload = {
        "q": normalize_text(text),
        "source": normalize_language_code(source_language),
        "target": normalize_language_code(target_language),
        "format": "text",
        "model": model,
    }
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()
    api_response = response.json()
    data = api_response.get("data", {})
    translations = data.get("translations", [])
    if not translations:
        raise ValueError("No translation returned from Google Cloud Translation API")
    translation = translations[0]
    return TranslationResponse(
        translated_text=translation.get("translatedText", ""),
        source_language=source_language,
        target_language=normalize_language_code(target_language),
        model_used=model,
        detected_source_language=translation.get("detectedSourceLanguage"),
    )
