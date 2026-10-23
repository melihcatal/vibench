import os

from google.cloud import translate_v2 as translate

from speech_models import TranscriptEvent, normalize_transcript


def live_caption_translate(event: TranscriptEvent, target_language: str = None) -> str:
    client = translate.Client()
    target = target_language or os.getenv("TRANSLATION_TARGET_LANGUAGE", "es")
    text = normalize_transcript(event.text)
    return client.translate(text, target_language=target)["translatedText"]
