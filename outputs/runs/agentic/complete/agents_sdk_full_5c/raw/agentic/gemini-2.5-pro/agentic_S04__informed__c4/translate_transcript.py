import os
from typing import List
import deepl
from speech_models import TranscriptSegment

def translate_segments(segments: List[TranscriptSegment], target_lang: str = "FR") -> List[str]:
    """
    Translates a list of transcript segments to a target language using DeepL.

    Args:
        segments: A list of TranscriptSegment objects.
        target_lang: The target language code (e.g., "FR" for French).

    Returns:
        A list of translated text strings.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    
    translator = deepl.Translator(auth_key)
    
    texts_to_translate = [segment.text for segment in segments]
    
    if not texts_to_translate:
        return []
        
    result = translator.translate_text(texts_to_translate, target_lang=target_lang)
    
    return [translation.text for translation in result]
