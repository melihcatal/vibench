import os
from security_client import get_deepl_translator
from security_models import TranslatedRunbook


def translate_runbook_notes(text: str, target_lang: str = "en") -> TranslatedRunbook:
    translator = get_deepl_translator()
    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return TranslatedRunbook(
            original_text=text,
            translated_text=result.text,
            source_lang=result.detected_source_lang,
            target_lang=target_lang,
        )
    except Exception as e:
        # In a real scenario, you might want to log the error or handle it more gracefully
        print(f"Error translating text: {e}")
        return TranslatedRunbook(
            original_text=text,
            translated_text=f"Translation failed: {e}",
            source_lang="N/A",
            target_lang=target_lang,
        )
