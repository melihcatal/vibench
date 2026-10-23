import os
from typing import List
import deepl


def translate_transcript(
    transcript_segments: List[str], target_lang: str = "ES", source_lang: str = "EN-US"
) -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")
    translator = deepl.Translator(auth_key)
    results = translator.translate_texts(
        transcript_segments,
        target_lang=deepl.TargetLanguage(target_lang),
        source_lang=deepl.LanguageCode(source_lang),
    )
    return [result.text for result in results]
