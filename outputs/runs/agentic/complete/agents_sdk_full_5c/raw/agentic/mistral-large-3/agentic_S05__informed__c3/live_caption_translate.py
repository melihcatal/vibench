import os
from google.cloud import translate_v2 as translate
from speech_models import TranscriptEvent

client = translate.Client()

def translate_caption(event: TranscriptEvent, target_language: str = "es") -> str:
    if not event.is_final:
        return ""
    result = client.translate(event.text, target_language=target_language)
    return result["translatedText"]