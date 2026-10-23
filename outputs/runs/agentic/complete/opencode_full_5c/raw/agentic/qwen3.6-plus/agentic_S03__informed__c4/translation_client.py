import os
import requests
from typing import Optional
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    BatchTranslationRequest,
    BatchTranslationResponse,
    MarkupTranslationRequest,
    DictionaryTranslationRequest,
    build_deepl_request_payload,
    parse_deepl_response,
)

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_URL_PRO = "https://api.deepl.com/v2/translate"


def get_deepl_api_key() -> str:
    api_key = os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    return api_key


def get_deepl_api_url() -> str:
    if os.environ.get("DEEPL_USE_PRO", "").lower() == "true":
        return DEEPL_API_URL_PRO
    return DEEPL_API_URL


def create_deepl_session() -> requests.Session:
    session = requests.Session()
    api_key = get_deepl_api_key()
    session.headers.update(
        {
            "Authorization": f"DeepL-Auth-Key {api_key}",
            "Content-Type": "application/json",
        }
    )
    return session


def translate_single(
    text: str,
    source_language: str,
    target_language: str,
    formality: Optional[str] = None,
    tag_handling: Optional[str] = None,
    preserve_formatting: bool = True,
) -> TranslationResponse:
    session = create_deepl_session()
    api_url = get_deepl_api_url()
    payload = build_deepl_request_payload(
        text=text,
        source_lang=source_language,
        target_lang=target_language,
        formality=formality,
        tag_handling=tag_handling,
        preserve_formatting=preserve_formatting,
    )
    response = session.post(api_url, json=payload)
    response.raise_for_status()
    return parse_deepl_response(response.json(), source_language, target_language)


def translate_batch(
    texts: list[str],
    source_language: str,
    target_language: str,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
) -> BatchTranslationResponse:
    session = create_deepl_session()
    api_url = get_deepl_api_url()
    results = []
    total_chars = 0
    for text in texts:
        payload = build_deepl_request_payload(
            text=text,
            source_lang=source_language,
            target_lang=target_language,
            formality=formality,
            preserve_formatting=preserve_formatting,
        )
        resp = session.post(api_url, json=payload)
        resp.raise_for_status()
        translation = parse_deepl_response(
            resp.json(), source_language, target_language
        )
        results.append(translation)
        total_chars += translation.character_count
    return BatchTranslationResponse(
        translations=results,
        total_characters=total_chars,
    )


def translate_markup(
    markup_text: str,
    source_language: str,
    target_language: str,
    tag_handling: str = "xml",
    ignore_tags: Optional[list[str]] = None,
    preserve_formatting: bool = True,
) -> TranslationResponse:
    session = create_deepl_session()
    api_url = get_deepl_api_url()
    payload = build_deepl_request_payload(
        text=markup_text,
        source_lang=source_language,
        target_lang=target_language,
        tag_handling=tag_handling,
        preserve_formatting=preserve_formatting,
    )
    if ignore_tags:
        payload["ignore_tags"] = ignore_tags
    response = session.post(api_url, json=payload)
    response.raise_for_status()
    return parse_deepl_response(response.json(), source_language, target_language)


def translate_dictionary_values(
    data: dict[str, str],
    source_language: str,
    target_language: str,
    formality: Optional[str] = None,
) -> dict[str, str]:
    session = create_deepl_session()
    api_url = get_deepl_api_url()
    translated_data = {}
    for key, value in data.items():
        payload = build_deepl_request_payload(
            text=value,
            source_lang=source_language,
            target_lang=target_language,
            formality=formality,
            preserve_formatting=True,
        )
        resp = session.post(api_url, json=payload)
        resp.raise_for_status()
        translation = parse_deepl_response(
            resp.json(), source_language, target_language
        )
        translated_data[key] = translation.translated_text
    return translated_data
