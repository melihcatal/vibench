from __future__ import annotations

from typing import Any, Dict

import deepl



def dashboard_note_translate(text: str, target_lang: str, source_lang: str | None = None) -> Dict[str, Any]:
    translator = deepl.Translator()
    result = translator.translate_text(text=text, target_lang=target_lang, source_lang=source_lang)
    return {
        "provider": "DeepL API",
        "target_lang": target_lang,
        "detected_source_lang": result.detected_source_lang,
        "translated_text": result.text,
    }
