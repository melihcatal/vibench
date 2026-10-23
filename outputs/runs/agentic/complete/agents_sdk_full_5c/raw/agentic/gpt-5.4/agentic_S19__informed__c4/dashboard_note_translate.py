from __future__ import annotations

from typing import Any, Dict, Optional

import deepl

from observability_models import TranslationResult


DEEPL_MODEL_PROVIDER = "DeepL API"


def dashboard_note_translate(text: str, target_language: str, source_language: Optional[str] = None) -> Dict[str, Any]:
    translator = deepl.Translator(auth_key=__import__("os").environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_language.upper(), source_lang=source_language.upper() if source_language else None)
    payload = TranslationResult(
        translated_text=result.text,
        source_language=getattr(result, "detected_source_lang", source_language),
        target_language=target_language.upper(),
    )
    return payload.__dict__
