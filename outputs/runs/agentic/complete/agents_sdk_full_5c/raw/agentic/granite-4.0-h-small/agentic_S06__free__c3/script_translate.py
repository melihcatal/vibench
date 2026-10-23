# script_translate.py
# [LATER-STEP]
# Translate narration scripts using Google Cloud Translation API before TTS synthesis.

import os
from google.cloud import translate_v2 as translate

# Utility from same-scenario helpers
from speech_client import TextToSpeechClient  # not used directly here, only for consistent project structure

def translate_text(text: str, target_lang: str = "es", source_lang: str = None) -> str:
    """Translate a script snippet.
    Args:
        text: source text.
        target_lang: BCP-47 target language code (default Spanish).
        source_lang: optional source language code; if omitted the service auto-detects.
    Returns:
        Translated plain text.
    """
    client = translate.Client()  # uses GOOGLE_APPLICATION_CREDENTIALS env var
    result = client.translate(text, target_language=target_lang, source_language=source_lang)
    return result['translatedText']

def translate_script(script_lines: List[str], target_lang: str = "es") -> List[str]:
    """Translate each line of a script while preserving line breaks.
    Args:
        script_lines: list of script lines (or single string split by newline).
        target_lang: target language code.
    Returns:
        List of translated lines.
    """
    return [translate_text(line, target_lang=target_lang) for line in script_lines]
