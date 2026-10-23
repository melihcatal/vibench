import os
from google.cloud import translate_v3 as translate
from typing import List, Dict

# Google Cloud Project ID can be set as an environment variable
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")


def translate_runbook_notes(
    text_to_translate: List[str],
    target_language_code: str,
    source_language_code: str = "en",
) -> List[Dict[str, str]]:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": text_to_translate,
            "mime_type": "text/plain",  # Mime type of the input text.
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append({"translated_text": translation.translated_text})
    return translations


# Example Usage
if __name__ == "main":
    try:
        runbook_notes = [
            "Rotate the database password every 90 days.",
            "Update the API key in the application configuration.",
        ]
        target_lang = "es"
        translated_notes = translate_runbook_notes(runbook_notes, target_lang)
        print(f"Translated notes to {target_lang}:")
        for note in translated_notes:
            print(f"- {note['translated_text']}")
    except Exception as e:
        print(f"Error translating runbook notes: {e}")
