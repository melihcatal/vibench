import os
import json
from typing import Dict
from safety_models import ModerationRequest, ModerationResponse, UnsafeSpan
# Use Google Cloud Translation API as concrete provider
import google.cloud.translate_v2 as translate
TRANSLATOR = translate.Client()

def translate_appeal(reply_text: str, target_lang: str = 'en') -> Dict[str, str]:
    """Translates appeal text into English for reviewer consumption."""
    result = TRANSLATOR.translate(reply_text, target_language=target_lang)
    return {
        'translated_text': result['translatedText'],
        'detected_source_language': result.get('detectedSourceLanguage', 'auto')
    }
