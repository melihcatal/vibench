import os
from google.cloud import translate_v2 as translate


def translate_alt_text(text: str, target_language: str = "es") -> str:
    translate_client = translate.Client()

    # Target can be BCP-47 language code (e.g. "es" for Spanish, "fr" for French)
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
