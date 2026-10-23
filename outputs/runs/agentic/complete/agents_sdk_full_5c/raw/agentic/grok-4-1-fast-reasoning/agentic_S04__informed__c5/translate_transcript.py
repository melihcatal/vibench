import os
import deepl
from typing import Optional

def translate_transcript(
    transcript: str,
    source_lang: str = "auto",
    target_lang: str = "EN-US"
) -> str:
    """
    Translate completed transcript segments using DeepL.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        transcript,
        source_lang=source_lang,
        target_lang=target_lang
    )
    return str(result)
