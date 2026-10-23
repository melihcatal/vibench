import os
from google.cloud import translate_v2 as translate

def translate_script(script: str, target_language: str = "es", source_language: str = "en") -> str:
    """
    Translates narration scripts before synthesis using Google Cloud Translation.
    """
    client = translate.Client()
    if source_language != "auto":
        result = client.translate(script, target_language=target_language, source_language=source_language)
    else:
        result = client.translate(script, target_language=target_language)
    return result["translatedText"]