from typing import Union
import deepl
from security_client import get_deepl_translator

def translate_compliance_note(text: str, target_lang: Union[str, deepl.TargetLanguage]):
    """
    Translates a compliance note into a specified language using the DeepL API.
    """
    translator = get_deepl_translator()

    if not text:
        return {"translation": "", "error": "No text provided."}

    try:
        # The DeepL Python library automatically handles source language detection.
        result = translator.translate_text(text, target_lang=target_lang)
        return {
            "translation": result.text,
            "detected_source_lang": result.detected_source_lang
        }
    except deepl.DeepLException as e:
        return {"translation": "", "error": str(e)}
    except Exception as e:
        return {"translation": "", "error": f"An unexpected error occurred: {e}"}
