from google.cloud import translate_v3 as translate

from translation_client import get_translation_client, parent_path
from translation_models import coerce_language, normalize_text


def translate_markup(text: str, source_language: str, target_language: str) -> str:
    client = get_translation_client()
    response = client.translate_text(
        request={
            "parent": parent_path(),
            "contents": [normalize_text(text)],
            "mime_type": "text/html",
            "source_language_code": coerce_language(source_language),
            "target_language_code": coerce_language(target_language),
        }
    )
    return response.translations[0].translated_text if response.translations else ""
