# [LATER-STEP] multilingual_query_translate.py
# Translate a query into English before multilingual embedding search

import os
from google.cloud import translate_v2 as translate
from typing import Tuple

# Initialize Google Cloud Translation client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)
translator = translate.Client()


def translate_query(query: str, target_lang: str = "en") -> Tuple[str, str]:
    """Translate a query text to the target language (default English).

    Returns a tuple (translated_query, source_language_code).
    """
    result = translator.translate(query, target_language=target_lang)
    return result["translatedText"], result["detectedSourceLanguage"]
