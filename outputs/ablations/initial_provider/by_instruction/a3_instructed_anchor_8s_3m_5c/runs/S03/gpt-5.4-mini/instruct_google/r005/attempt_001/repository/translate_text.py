from google.cloud import translate_v3 as translate

from translation_client import get_translation_client, parent_path
from translation_models import TranslationRequest, coerce_language, normalize_text


def translate_text(text: str, source_language: str, target_language: str) -> str:
    request = TranslationRequest(
        source_language=coerce_language(source_language),
        target_language=coerce_language(target_language),
        text=normalize_text(text),
    )
    client = get_translation_client()
    response = client.translate_text(
        request={
            "parent": parent_path(),
            "contents": [request.text],
            "mime_type": request.mime_type,
            "source_language_code": request.source_language,
            "target_language_code": request.target_language,
        }
    )
    return response.translations[0].translated_text if response.translations else ""
