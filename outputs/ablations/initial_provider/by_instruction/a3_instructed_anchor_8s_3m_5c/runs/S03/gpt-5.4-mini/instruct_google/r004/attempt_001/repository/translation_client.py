import os
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from google.cloud import translate_v3 as translate

from translation_models import normalize_text, normalize_texts


def get_project_id() -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    return project_id


def get_location() -> str:
    return os.getenv("GOOGLE_CLOUD_TRANSLATE_LOCATION", "global")


def create_client() -> translate.TranslationServiceClient:
    return translate.TranslationServiceClient()


def parent_path() -> str:
    return f"projects/{get_project_id()}/locations/{get_location()}"


def translate_text_value(text: str, target_language: str, source_language: str | None = None) -> str:
    client = create_client()
    response = client.translate_text(
        request={
            "parent": parent_path(),
            "contents": [normalize_text(text)],
            "mime_type": "text/plain",
            "target_language_code": target_language,
            **({"source_language_code": source_language} if source_language else {}),
        }
    )
    return response.translations[0].translated_text if response.translations else ""


def translate_texts_value(texts: Sequence[str], target_language: str, source_language: str | None = None) -> List[str]:
    normalized = normalize_texts(texts)
    if not normalized:
        return []
    client = create_client()
    response = client.translate_text(
        request={
            "parent": parent_path(),
            "contents": normalized,
            "mime_type": "text/plain",
            "target_language_code": target_language,
            **({"source_language_code": source_language} if source_language else {}),
        }
    )
    return [item.translated_text for item in response.translations]


def translate_markup_value(markup: str, target_language: str, source_language: str | None = None) -> str:
    client = create_client()
    response = client.translate_text(
        request={
            "parent": parent_path(),
            "contents": [normalize_text(markup)],
            "mime_type": "text/html",
            "target_language_code": target_language,
            **({"source_language_code": source_language} if source_language else {}),
        }
    )
    return response.translations[0].translated_text if response.translations else ""


def translate_dictionary_values_value(payload: Mapping[str, Any], target_language: str, source_language: str | None = None) -> Dict[str, str]:
    keys = list(payload.keys())
    values = normalize_texts(list(payload.values()))
    translated_values = translate_texts_value(values, target_language, source_language)
    return {key: translated_values[index] if index < len(translated_values) else "" for index, key in enumerate(keys)}
