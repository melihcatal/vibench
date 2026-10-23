import os
from google.cloud import translate_v2 as translate

def alt_text_translate(text: str, target_language: str, config=None):
    config = config or {}
    translate_client = translate.Client()

    # Target can be a language code or a language name.
    # E.g. "fr" for French, "es" for Spanish, or "hindi" for Hindi.
    result = translate_client.translate(
        text,
        target_language=target_language
    )

    return {"translated_text": result["translatedText"]}
