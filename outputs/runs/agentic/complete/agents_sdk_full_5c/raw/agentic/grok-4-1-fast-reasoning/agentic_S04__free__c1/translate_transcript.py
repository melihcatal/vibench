import os
from typing import List
from deepl import Translator

def translate_transcript(segments: List[str], target_lang: str = 'EN-US') -> List[str]:
    api_key = os.getenv('DEEPL_API_KEY')
    if not api_key:
        raise ValueError('DEEPL_API_KEY environment variable is required.')
    translator = Translator(api_key)
    return [translator.translate_text(segment, target_lang=target_lang).text for segment in segments]