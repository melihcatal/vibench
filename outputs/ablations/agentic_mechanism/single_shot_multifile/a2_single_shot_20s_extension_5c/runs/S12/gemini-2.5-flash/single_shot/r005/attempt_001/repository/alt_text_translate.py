import os
from google.cloud import translate_v3
from google.cloud.translate_v3 import types
from vision_client import get_google_translation_client
from vision_models import TranslatedText

def translate_alt_text(text: str, target_language_code: str, source_language_code: str = "en") -> TranslatedText:
    client = get_google_translation_client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set for Google Cloud Translation.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
        source_language_code=source_language_code,
    )

    if response.translations:
        translation = response.translations[0]
        return TranslatedText(text=translation.translated_text, language_code=target_language_code)
    else:
        raise Exception("Translation failed or returned no results.")