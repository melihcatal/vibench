import os
from typing import List, Optional

import deepl

def translate_transcript_segments(
    segments: List[str],
    target_lang: str = 'ES',
    auth_key: Optional[str] = None
) -> List[str]:
    if auth_key is None:
        auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key)
    results = translator.translate_text(segments, target_lang=target_lang)
    return [result.text for result in results]