import os
import deepl
from typing import Optional


def translate_transcript(transcript_text: str, target_lang: str = "ES") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(transcript_text, target_lang=target_lang)
    return result.text
