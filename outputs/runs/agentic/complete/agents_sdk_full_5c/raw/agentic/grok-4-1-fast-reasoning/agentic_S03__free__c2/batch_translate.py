import os
from typing import List
from google.cloud import translate_v2 as translate

def batch_translate(texts: List[str], source_lang: str, target_lang: str) -> List[str]:
    client = translate.Client()
    results = client.translate(texts, source_language=source_lang, target_language=target_lang)
    return [r['translatedText'] for r in results]
