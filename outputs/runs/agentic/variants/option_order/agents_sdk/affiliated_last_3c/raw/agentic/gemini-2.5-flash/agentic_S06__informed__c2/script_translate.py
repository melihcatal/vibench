from google.cloud import translate_v2 as translate
import os
from typing import List, Dict, Any

def translate_text(text: str, target_language: str, source_language: str = None) -> Dict[str, Any]:
    """Translates narration scripts using Google Cloud Translation."""
    client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language, source_language=source_language)

    return result

