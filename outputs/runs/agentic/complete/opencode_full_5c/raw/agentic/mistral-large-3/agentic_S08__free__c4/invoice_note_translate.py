from typing import Optional
from google.cloud import translate_v2 as translate
import os


def translate_invoice_note(
    text: Optional[str], target_language: str = "en"
) -> Optional[str]:
    if not text:
        return None

    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
