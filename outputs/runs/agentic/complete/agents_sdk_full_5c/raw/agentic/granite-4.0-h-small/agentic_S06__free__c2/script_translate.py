# [LATER-STEP] script_translate.py

from typing import Optional
from google.cloud import translate_v2 as translate

def translate_script(script: str, target_lang: str = "en") -> str:
    """Translate a narration script to the target language using Google Cloud Translation API.

    Args:
        script: Raw narration text.
        target_lang: BCP-47 language code (e.g., 'es'). Default 'en' returns original.

    Returns:
        Translated script ready for TTS synthesis.
    """
    # Instantiate client with env creds; no explicit key needed.
    translator = translate.Client()
    result = translator.translate(script, target_language=target_lang)
    return result["translatedText"]
