import os
from typing import List, Dict, Any
from speech_client import SpeechClient
from speech_models import NormalizedTranscript, normalize_timestamps
from google.cloud import translate_v2 as translate

TRANSLATOR = translate.Client()  # uses GOOGLE_APPLICATION_CREDENTIALS env var


def translate_transcript(
    segments: NormalizedTranscript, target_lang: str = "es"
) -> List[str]:
    """Translates a list of timestamped segments into the target language using DeepL.
    Returns a list of translated text strings, preserving original order.
    """
    texts = [seg["text"] for seg in segments]
    # DeepL Python SDK auto-detects source language
    translation = TRANSLATOR.translate(" ".join(texts), target_language=target_lang)
    translated_text = translation["text"]
    # Split by whitespace—basic split for demo; more robust splitting may be added
    return translated_text.split()
