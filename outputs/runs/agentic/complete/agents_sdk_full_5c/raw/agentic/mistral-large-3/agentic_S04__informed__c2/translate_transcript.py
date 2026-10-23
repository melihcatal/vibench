import os
from typing import List
from google.cloud import translate_v2 as translate

def translate_transcript(text_segments: List[str], target_language: str = "es") -> List[str]:
    """
    Translate transcript segments using Google Cloud Translation API.
    Returns a list of translated text segments.
    """
    client = translate.Client()
    translations = []
    for segment in text_segments:
        result = client.translate(segment, target_language=target_language)
        translations.append(result["translatedText"])
    return translations