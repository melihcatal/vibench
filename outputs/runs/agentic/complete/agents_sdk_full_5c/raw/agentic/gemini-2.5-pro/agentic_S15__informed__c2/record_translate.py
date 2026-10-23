import os
import deepl
from typing import Dict

def translate_record_fields(record: Dict[str, any], target_language: str = "DE") -> Dict[str, any]:
    """
    Translates user-facing fields of a document record using the DeepL API.

    Args:
        record: A dictionary representing the document record.
        target_language: The target language code (e.g., "DE" for German).

    Returns:
        A new dictionary with the 'content' field translated.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        # The deepl.Translator class is the main entry point for the SDK
        translator = deepl.Translator(auth_key)
        
        text_to_translate = record.get("content")
        if not text_to_translate:
            return record

        # The translate_text method performs the translation
        result = translator.translate_text(text_to_translate, target_lang=target_language)
        
        translated_record = record.copy()
        translated_record["content_translated"] = result.text
        translated_record["detected_source_lang"] = result.detected_source_lang
        
        return translated_record

    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        return record
