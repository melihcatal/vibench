import os
from typing import List
from google.cloud import translate_v2 as translate

def log_message_translate(messages: List[str], target_language: str = "es") -> List[str]:
    client = translate.Client()
    results = client.translate(
        messages,
        target_language=target_language
    )
    return [r['translatedText'] for r in results]
