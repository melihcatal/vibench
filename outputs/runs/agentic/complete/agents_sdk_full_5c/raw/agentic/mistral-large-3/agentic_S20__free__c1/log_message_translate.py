from typing import List
from google.cloud import translate_v2 as translate
import os

def translate_log_messages(log_messages: List[str], target_language: str = "es") -> List[dict]:
    """
    Translate support-visible log messages using Google Cloud Translation API.
    """
    client = translate.Client()
    results = []
    
    for message in log_messages:
        result = client.translate(
            message,
            target_language=target_language
        )
        results.append({
            "original": message,
            "translated": result["translatedText"]
        })
    
    return results