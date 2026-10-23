# Translate encryption/compliance notes for reviewer consumption.
# Uses DeepL API for professional translation.
# Requires DEEPL_AUTH_KEY env var.

import os
import deepl

def translate_to_target(text: str, target_lang: str = 'EN') -> str:
    """Translate text (e.g., compliance notes) using DeepL.",
    translator = deepl.Translator(os.getenv('DEEPL_AUTH_KEY'))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
