# [LATER-STEP] script_translate.py
# Translate narration scripts before synthesis using Google Cloud Translation API

from google.cloud import translate_v2 as translate


def translate_script(script: str, target_lang: str = "es") -> str:
    """Translates the entire script to the target language."""
    client = translate.Client()
    result = client.translate(script, target_language=target_lang)
    return result["translatedText"]
