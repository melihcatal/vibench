import os
from typing import List
from google.cloud import translate_v3

from safety_client import get_google_translate_client
from safety_models import TranslatedText

def translate_appeal_text(text: str, target_language: str = "en") -> TranslatedText:
    client = get_google_translate_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    # The project ID and location of the file to be translated
    # Location must be a region like 'global' or 'us-central1'
    parent = f"projects/{project_id}/locations/global"

    # Translate text from source language to target language
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            # "source_language_code": "auto" # Auto-detect source language
        }
    )

    translated_text_content = response.translations[0].translated_text
    source_language_code = response.translations[0].detected_language_code

    return TranslatedText(
        original_text=text,
        translated_text=translated_text_content,
        source_language=source_language_code,
        target_language=target_language
    )
