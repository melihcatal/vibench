import os
import re
from typing import Optional
from translation_models import (
    MarkupTranslationRequest,
    TranslationResponse,
    normalize_language_code,
)
from translation_client import (
    GoogleTranslationClient,
    GOOGLE_TRANSLATE_API_KEY,
    GOOGLE_TRANSLATE_API_ENDPOINT,
    DEFAULT_GOOGLE_MODEL,
    create_translation_client,
)


def translate_markup(
    markup_text: str,
    source_language: str,
    target_language: str,
    model: str = DEFAULT_GOOGLE_MODEL,
    preserve_formatting: bool = True,
    api_key: Optional[str] = None,
) -> TranslationResponse:
    key = api_key or GOOGLE_TRANSLATE_API_KEY
    client = create_translation_client(api_key=key)
    request = MarkupTranslationRequest(
        markup_text=markup_text,
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language),
        model=model,
        preserve_formatting=preserve_formatting,
    )
    return client.translate_html(request)


def extract_and_translate_segments(
    markup_text: str,
    source_language: str,
    target_language: str,
    model: str = DEFAULT_GOOGLE_MODEL,
    api_key: Optional[str] = None,
) -> str:
    tag_pattern = re.compile(r"(<[^>]+>)")
    segments = tag_pattern.split(markup_text)
    translated_segments = []
    for segment in segments:
        if tag_pattern.match(segment):
            translated_segments.append(segment)
        elif segment.strip():
            key = api_key or GOOGLE_TRANSLATE_API_KEY
            client = create_translation_client(api_key=key)
            request = MarkupTranslationRequest(
                markup_text=segment,
                source_language=normalize_language_code(source_language),
                target_language=normalize_language_code(target_language),
                model=model,
            )
            response = client.translate_html(request)
            translated_segments.append(response.translated_text)
        else:
            translated_segments.append(segment)
    return "".join(translated_segments)


def translate_markup_via_http(
    markup_text: str,
    source_language: str,
    target_language: str,
    model: str = DEFAULT_GOOGLE_MODEL,
    api_key: Optional[str] = None,
) -> TranslationResponse:
    import requests

    key = api_key or os.environ.get("GOOGLE_TRANSLATE_API_KEY", "")
    endpoint = GOOGLE_TRANSLATE_API_ENDPOINT
    payload = {
        "q": markup_text,
        "source": normalize_language_code(source_language),
        "target": normalize_language_code(target_language),
        "format": "html",
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
