import os
from typing import List, Dict
import deepl

def translate_transcript(segments: List[Dict[str, str]], target_lang: str = "DE") -> List[Dict[str, str]]:
    """
    Translates transcript segments using DeepL API.
    Returns translated segments with original metadata.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    
    translator = deepl.Translator(auth_key)
    
    translated_segments = []
    for segment in segments:
        result = translator.translate_text(
            segment["text"],
            target_lang=target_lang
        )
        translated_segments.append({
            **segment,
            "text": result.text
        })
    
    return translated_segments