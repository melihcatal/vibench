import os
from google.cloud import translate_v3
from typing import Optional

from safety_client import get_google_translate_client
from safety_models import TranslationInput, TranslationOutput

def translate_appeal_text(translation_input: TranslationInput) -> TranslationOutput:
    client = get_google_translate_client()
    project_id = os.getenv("GOOGLE_TRANSLATE_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_TRANSLATE_PROJECT_ID environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [translation_input.text],
                "target_language_code": translation_input.target_language,
                "source_language_code": translation_input.source_language, # Optional
                "mime_type": "text/plain",  # Mime type of the input text
            }
        )

        translated_text = ""
        detected_source_language = None

        if response.translations:
            translated_text = response.translations[0].translated_text
            detected_source_language = response.translations[0].detected_language_code
        
        return TranslationOutput(translated_text=translated_text, detected_source_language=detected_source_language)
    except Exception as e:
        print(f"Error translating appeal text with Google Translate: {e}")
        return TranslationOutput(translated_text="Translation failed.", detected_source_language=None)
