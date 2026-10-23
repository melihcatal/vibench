import os
import html
from translation_client import create_translator_client
from translation_models import TranslationResponse

def translate_dictionary_values(src_dict: dict, target_lang: str = "es") -> dict:
    """Translate all string values in a dictionary while preserving keys.",
    translator = create_translator_client()
    translated = {}
    for k, v in src_dict.items():
        if isinstance(v, str):
            resp = translator.translate(
                texts=[v],
                to_language=target_lang
            )
            translated[k] = TranslationResponse(resp[0]).get_translated_text()
        else:
            translated[k] = v
    return translated
