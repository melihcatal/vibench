import os
from speech_models import normalize_voices, VoiceInfo
from google.cloud import translate_v2 as translate

SDK_PROVIDER = "Google"

# Ensure the GOOGLE_APPLICATION_CREDENTIALS env var is set
goog_cred = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not goog_cred:
    raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS not configured")

client = translate.Client()

def translate_text(text: str, target_lang: str = "fr") -> str:
    """Translate plain text using Google Cloud Translation.
    Returns the translated string.
    """
    result = client.translate(text, target_language=target_lang)
    return result["translatedText"]

# Example with voice selection after translation could be done via select_voice.py
