from typing import Dict, Any
import os
from google.cloud import translate_v2 as translate


def translate_invoice_note(text: str, target_language: str = "en") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]