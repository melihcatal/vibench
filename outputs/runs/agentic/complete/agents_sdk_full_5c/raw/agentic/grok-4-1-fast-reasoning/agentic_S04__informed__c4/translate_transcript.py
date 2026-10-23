import os
import deepl
from typing import List

def translate_transcript(segments: List[str], target_lang: str = "EN-US") -> List[str]:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    if not auth_key:
        raise ValueError('DEEPL_AUTH_KEY environment variable is required.')
    translator = deepl.Translator(auth_key)
    results = translator.translate_text(segments, target_lang=deepl.TargetLanguage(target_lang))
    return [result.text for result in results]