# LATER-STEP

import os
from typing import Dict

# Provider selection: Google Cloud Translation (REST) for translating dashboard/metric notes

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"


def translate_note(text: str, target_language: str = "es") -> Dict:
    """Translate a metric or dashboard note into another locale using Google Cloud Translation.

    Args:
        text (str): Original note text.
        target_language (str): ISO 639‑1 language code (default 'es' for Spanish).

    Returns:
        Dict: JSON response from Google Translation API containing translated text.
    """
    import requests, json

    payload = {
        "q": text,
        "target": target_language,
        "format": "text",
    }
    resp = requests.post(
        TRANSLATE_ENDPOINT,
        json=payload,
        params={"key": os.getenv("GOOGLE_APPLICATION_CREDENTIALS")},
    )
    resp.raise_for_status()
    return resp.json()


# Example (non‑executing):
# result = translate_note('Disk latency high', 'fr')
# print(result['data']['translations'][0]['translatedText'])
