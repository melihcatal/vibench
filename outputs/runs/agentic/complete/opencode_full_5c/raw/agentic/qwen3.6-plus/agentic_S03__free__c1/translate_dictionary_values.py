import os
from typing import Dict, Optional
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
    normalize_language_code,
)
from translation_client import (
    GoogleTranslationClient,
    GOOGLE_TRANSLATE_API_KEY,
    GOOGLE_TRANSLATE_API_ENDPOINT,
    DEFAULT_GOOGLE_MODEL,
    create_translation_client,
)


def translate_dictionary_values(
    data: Dict[str, str],
    source_language: str,
    target_language: str,
    model: str = DEFAULT_GOOGLE_MODEL,
    api_key: Optional[str] = None,
) -> DictionaryTranslationResponse:
    key = api_key or GOOGLE_TRANSLATE_API_KEY
    client = create_translation_client(api_key=key)
    request = DictionaryTranslationRequest(
        data=data,
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language),
        model=model,
    )
    return client.translate_dictionary(request)


def translate_dictionary_values_via_http(
    data: Dict[str, str],
    source_language: str,
    target_language: str,
    model: str = DEFAULT_GOOGLE_MODEL,
    api_key: Optional[str] = None,
) -> DictionaryTranslationResponse:
    import requests

    key = api_key or os.environ.get("GOOGLE_TRANSLATE_API_KEY", "")
    endpoint = GOOGLE_TRANSLATE_API_ENDPOINT
    values = list(data.values())
    keys = list(data.keys())
    payload = {
        "q": values,
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
    translated_data = {}
    translations = api_response.get("data", {}).get("translations", [])
    for i, t_key in enumerate(keys):
        if i < len(translations):
            translated_data[t_key] = translations[i].get("translatedText", "")
        else:
            translated_data[t_key] = data[t_key]
    return DictionaryTranslationResponse(
        translated_data=translated_data,
        original_keys=keys,
        target_language=normalize_language_code(target_language),
    )
