import os
from security_client import SecurityClients
from security_models import TranslationResult
import deepl

def translate_runbook_notes(text_to_translate: str, target_lang: str = "EN-US", source_lang: str = None) -> TranslationResult:
    translator = SecurityClients.get_deepl_translator()
    try:
        result = translator.translate_text(
            text_to_translate,
            source_lang=source_lang,
            target_lang=target_lang
        )
        return TranslationResult(
            original_text=text_to_translate,
            translated_text=result.text,
            source_lang=result.detected_source_lang,
            target_lang=target_lang
        )
    except deepl.exceptions.DeepLException as e:
        raise RuntimeError(f"DeepL API error during translation: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during translation: {e}")