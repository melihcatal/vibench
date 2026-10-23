import os
import deepl
from typing import Dict, Any
from document_client import DocumentAIClient

def translate_invoice_note(text: str, target_lang: str = "en") -> Dict[str, Any]:
    translator = DocumentAIClient().get_deepl_translator()

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return {"success": True, "original_text": text, "translated_text": result.text, "detected_source_lang": result.detected_source_lang}
    except deepl.exceptions.DeepLException as e:
        return {"success": False, "error": str(e)}
