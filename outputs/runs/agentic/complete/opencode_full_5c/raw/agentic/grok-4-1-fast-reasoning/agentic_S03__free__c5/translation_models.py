from typing import Dict, Any
from deepl import Translation


def parse_translation(result: Translation) -> Dict[str, Any]:
    return {
        "translated_text": result.text,
        "detected_source_lang": getattr(result, "detected_lang", None),
    }


def normalize_text(text: str) -> str:
    return text.strip()
