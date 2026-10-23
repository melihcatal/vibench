import os
from typing import Any, Dict

from google.cloud import translate_v3 as translate

from translation_models import (
    TranslationRequest,
    TranslationResponse,
    normalize_mapping_values,
    normalize_text,
    normalize_text_list,
)


def load_translation_config() -> Dict[str, str]:
    return {
        "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        "location": os.environ.get("GOOGLE_CLOUD_TRANSLATION_LOCATION", "global"),
    }


def get_translate_client() -> translate.TranslationServiceClient:
    return translate.TranslationServiceClient()


def translate_single_text(request: TranslationRequest) -> TranslationResponse:
    cfg = load_translation_config()
    client = get_translate_client()
    parent = f"projects/{cfg['project_id']}/locations/{cfg['location']}"
    resp = client.translate_text(
        contents=[normalize_text(request.source_text)],
        target_language_code=request.target_language,
        source_language_code=request.source_language,
        parent=parent,
        mime_type="text/plain",
    )
    return TranslationResponse(
        resp.translations[0].translated_text if resp.translations else "",
        request.source_language,
        request.target_language,
        "google-cloud-translate",
    )


def translate_text_list(values, source_language: str, target_language: str):
    cfg = load_translation_config()
    client = get_translate_client()
    parent = f"projects/{cfg['project_id']}/locations/{cfg['location']}"
    resp = client.translate_text(
        contents=normalize_text_list(values),
        target_language_code=target_language,
        source_language_code=source_language,
        parent=parent,
        mime_type="text/plain",
    )
    return [t.translated_text for t in resp.translations]


def translate_html_text(
    html_text: Any, source_language: str, target_language: str
) -> str:
    cfg = load_translation_config()
    client = get_translate_client()
    parent = f"projects/{cfg['project_id']}/locations/{cfg['location']}"
    resp = client.translate_text(
        contents=[normalize_text(html_text)],
        target_language_code=target_language,
        source_language_code=source_language,
        parent=parent,
        mime_type="text/html",
    )
    return resp.translations[0].translated_text if resp.translations else ""


def translate_dictionary_values(
    values: Dict[str, Any], source_language: str, target_language: str
) -> Dict[str, str]:
    cfg = load_translation_config()
    client = get_translate_client()
    parent = f"projects/{cfg['project_id']}/locations/{cfg['location']}"
    normalized = normalize_mapping_values(values)
    resp = client.translate_text(
        contents=list(normalized.values()),
        target_language_code=target_language,
        source_language_code=source_language,
        parent=parent,
        mime_type="text/plain",
    )
    return dict(zip(normalized.keys(), [t.translated_text for t in resp.translations]))
