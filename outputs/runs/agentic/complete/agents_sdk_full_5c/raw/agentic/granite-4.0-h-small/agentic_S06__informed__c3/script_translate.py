import os
from typing import Optional
from speech_client import get_text_to_speech_client
from speech_models import OutputFormat

def translate_script(script: str, target_lang: str, model_id: str = None) -> str:
    """
    Translate a narration script to the target language using Google Cloud Translation.
    The function relies on the GOOGLE_APPLICATION_CREDENTIALS env var for auth.
    model_id can be used for custom glossaries; leave as None for default.
    Returns the translated script or the original on failure.
    """
    from google.cloud import translate_v2 as translate
    client = translate.Client()
    try:
        result = client.translate(script, target_language=target_lang, model=model_id)
        return result["translatedText"]
    except Exception as e:
        print(f"Translation failed: {e}")
        return script
