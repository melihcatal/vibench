# script_translate.py
import os
from google.cloud import translate_v2 as translate


# Use GOOGLE_APPLICATION_CREDENTIALS env var for auth
def translate_script(script, target="es"):
    """Translate a plain text narration script to the target language."""
    client = translate.Client()
    result = client.translate(script, target_language=target)
    return result["translatedText"]
