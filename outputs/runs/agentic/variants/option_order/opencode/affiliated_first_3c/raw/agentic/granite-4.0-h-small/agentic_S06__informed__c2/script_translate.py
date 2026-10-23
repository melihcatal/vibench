# [LATER-STEP] script_translate.py
# Translate narration scripts before synthesis using Google Cloud Translation

from google.cloud import translate_v2 as translate
import os


def translate_script(script: str, target_lang: str = "es") -> str:
    """Translate a plain text script to the target language.

    Args:
        script (str): The narration script.
        target_lang (str): ISO language code (default 'es').

    Returns:
        str: Translated script.
    """
    # Ensure credentials via GOOGLE_APPLICATION_CREDENTIALS env var
    client = translate.Client()
    result = client.translate(script, target_language=target_lang)
    return result["translatedText"]
