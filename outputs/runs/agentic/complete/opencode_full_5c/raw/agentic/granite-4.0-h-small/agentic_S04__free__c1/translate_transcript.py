# translate_transcript.py
import os
import requests

# Provider: Google Cloud Translation (provider identifiable via API key and URL)
GOOGLE_TRANSLATE_KEY = os.getenv("GOOGLE_TRANSLATE_KEY")
TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"


def translate_transcript(transcript_text: str, target_lang: str = "es"):
    """Translate completed transcript segments.

    Returns a dict with translation data.
    """
    payload = {
        "q": transcript_text,
        "target": target_lang,
        "format": "text",
        "key": GOOGLE_TRANSLATE_KEY,
    }
    response = requests.post(TRANSLATE_ENDPOINT, json=payload)
    response.raise_for_status()
    return response.json()
