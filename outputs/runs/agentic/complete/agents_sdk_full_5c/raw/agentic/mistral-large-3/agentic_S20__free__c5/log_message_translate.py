from typing import List
import os
from google.cloud import translate_v2 as translate

def translate_log_messages(log_messages: List[str], target_language: str = "es") -> List[dict]:
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