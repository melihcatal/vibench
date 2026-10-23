from __future__ import annotations

from typing import Dict
import os

from deepl import DeepLClient



def translate_runbook_notes(text: str, target_language: str) -> Dict[str, str]:
    client = DeepLClient(os.getenv("DEEPL_API_KEY"))
    result = client.translate_text(text, target_lang=target_language)
    return {
        "provider": "DeepL",
        "target_language": target_language,
        "translated_text": result.text,
        "detected_source_language": getattr(result, "detected_source_lang", ""),
    }
