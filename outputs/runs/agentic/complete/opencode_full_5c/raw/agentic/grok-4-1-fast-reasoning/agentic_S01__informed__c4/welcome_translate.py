from google.cloud import translate_v2 as translate
from typing import Dict, Any


def translate_welcome_copy(copy_text: str, target_locale: str) -> str:
    client = translate.Client()
    result = client.translate(copy_text, target_language=target_locale)
    return result["translatedText"]
