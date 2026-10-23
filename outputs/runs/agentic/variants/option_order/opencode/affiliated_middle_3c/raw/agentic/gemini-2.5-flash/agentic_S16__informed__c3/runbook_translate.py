import os
from google.cloud import translate_v2 as translate
from typing import List


def translate_runbook_notes(notes: List[str], target_language: str = "en") -> List[str]:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        # If GOOGLE_APPLICATION_CREDENTIALS is not set, the client library will look for it
        # in the default locations or try to use default application credentials.
        # For explicit control or if running outside GCP environment, consider setting this.
        pass

    client = translate.Client()

    translations = []
    for note in notes:
        try:
            result = client.translate(note, target_language=target_language)
            translations.append(result["translatedText"])
        except Exception as e:
            translations.append(f"Translation failed for '{note}': {e}")
    return translations
