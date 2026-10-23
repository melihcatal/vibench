import os
import deepl
from typing import List


def translate_transcript(
    transcript_segments: List[str], target_language: str = "FR"
) -> List[str]:
    """
    Translates completed transcript segments using DeepL.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(transcript_segments, target_lang=target_language)

    if isinstance(result, list):
        return [translation.text for translation in result]
    else:
        return [result.text]
