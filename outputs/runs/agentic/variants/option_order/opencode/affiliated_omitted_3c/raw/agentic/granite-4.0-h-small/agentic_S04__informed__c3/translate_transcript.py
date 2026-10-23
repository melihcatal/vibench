# Translate completed transcript segments
import os
import requests
from speech_models import TranscribeResponse

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
DEEPL_BASE_URL = "https://api.deepl.com/v2/translate"


def translate_transcript(transcript_uri, target_lang="es", preserve_formatting=True):
    """Download transcript from S3 (placeholder), then translate via DeepL API.","""
    # Placeholder: fetch transcript text (normally download from S3)
    transcript_text = "This is an example transcript that we want to translate."
    payload = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": transcript_text,
        "target_lang": target_lang,
        "preserve_formatting": str(preserve_formatting).lower(),
    }
    response = requests.post(DEEPL_BASE_URL, data=payload)
    if response.status_code == 200:
        data = response.json()
        translated = data["translations"][0]["text"]
        return translated
    else:
        raise RuntimeError(
            f"Translation failed: {response.status_code} {response.text}"
        )
