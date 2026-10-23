# [LATER-STEP] dashboard_note_translate.py

# Translate metric or dashboard notes for another locale using a public translation API.
# In this example we use Google Cloud Translation as the concrete provider.

from __future__ import annotations
from datetime import datetime
import os
import json
import requests

# Google Cloud Translation client libraries are imported for SDK usage.
# from google.cloud import translate_v2 as translate
# client = translate.Client()

# For the purpose of this script we call the REST API directly.
# Set environment variable GOOGLE_APPLICATION_CREDENTIALS to point at a service account JSON.
# Also set TARGET_LOCALE (e.g., "es", "fr", "de").


def translate_note(
    note_id: str, target_locale: str = os.getenv("TARGET_LOCALE", "es")
) -> dict:
    """
    Translate a dashboard/metric note identified by note_id to the target language.

    Parameters:
        note_id: Identifier of the note (e.g., New Relic note GUID).
        target_locale: ISO language code, defaults to environment variable TARGET_LOCALE.

    Returns:
        dict with keys: original_note, translated_note, target_locale, status.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Google Cloud Translation API key not found in environment variable GOOGLE_API_KEY"
        )

    url = (
        "https://translation.googleapis.com/v3/projects"
        f"/-/locations/global/translateText"
    )
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    # Example payload – New Relic note content is supplied in `source_text`.
    payload = {
        "sourceLanguageCode": "en",
        "targetLanguageCode": target_locale,
        "sourceText": f"Note {note_id} content placeholder",
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    # The API returns translatedText; attach IDs for context.
    return {
        "original_note": payload["sourceText"],
        "translated_note": result.get("translatedText", ""),
        "target_locale": target_locale,
        "status": "success",
    }


if __name__ == "__main__":
    # Placeholder note ID – in a real implementation this would be retrieved from New Relic.
    sample_id = "nr_note_001"
    translation = translate_note(sample_id, target_locale="fr")
    print(json.dumps(translation, indent=2))
