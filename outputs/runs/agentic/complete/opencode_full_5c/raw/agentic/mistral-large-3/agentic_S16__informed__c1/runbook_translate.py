from typing import Dict, Optional
import os
import deepl


def translate_runbook_notes(
    runbook_notes: str, target_lang: str = "EN-US"
) -> Optional[Dict[str, str]]:
    """
    Translates secret-rotation runbook notes using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DeepL authentication key not configured.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(runbook_notes, target_lang=target_lang)

        return {
            "original_text": runbook_notes,
            "translated_text": result.text,
            "detected_source_language": result.detected_source_lang,
            "target_language": target_lang,
        }
    except Exception as e:
        print(f"Failed to translate runbook notes: {e}")
        return None
