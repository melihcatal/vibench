import os
import requests
from google.cloud import translate_v2 as translate

# Google Cloud Translation client configured via environment variable
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS env var not set")

def translate_transcript(segment: str, target_lang: str = "es") -> str:
    """Translate a single transcript segment using Google Cloud Translation.
    Returns the translated text.
    """
    client = translate.Client()
    result = client.translate(segment, target_language=target_lang)
    return result["translatedText"]
