import os
from typing import Dict
from google.cloud import translate_v2 as translate


def translate_narration(script: str, target_lang: str = "es-ES") -> str:
    """Translate narration script to target language using Google Cloud Translation.

    Returns the translated plain text.
    """
    client = translate.Client()
    result = client.translate(script, target_language=target_lang)
    return result["translatedText"]


# Optional helper to detect language before translation
# from google.cloud import language_v1
# def detect_language(text: str) -> str:
#     client = language_v1.LanguageServiceClient()
#     response = client.analyze_sentiment(
#         request={"document": {"type_": "PLAIN_TEXT", "content": text}}
#     )
#     lang = response.language
#     return lang
