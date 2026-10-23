
import os
from google.cloud import translate_v3 as translate
from document_client import get_translation_client
from document_models import DocumentTranslation

def ocr_translate(payload, config=None):
    config = config or {}
    client = get_translation_client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global") # For translation, global is common
    target_language = config.get("TARGET_LANGUAGE", "es") # Default to Spanish if not provided

    if not project_id:
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT environment variable.")

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[payload['text']],
        target_language_code=target_language,
        mime_type="text/plain",
    )

    translations = []
    for translation in response.translations:
        translations.append(DocumentTranslation(translated_text=translation.translated_text))

    return translations[0] if translations else DocumentTranslation(translated_text="")
