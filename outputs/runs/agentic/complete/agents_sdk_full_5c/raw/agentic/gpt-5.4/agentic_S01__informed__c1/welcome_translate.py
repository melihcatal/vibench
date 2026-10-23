from __future__ import annotations

import os
from typing import Dict, Optional

import deepl

from identity_models import TranslationResult


def welcome_translate(text: str, target_locale: str, source_locale: Optional[str] = None) -> Dict[str, Optional[str]]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_locale.upper(),
        source_lang=source_locale.upper() if source_locale else None,
        model_type="prefer_quality_optimized",
    )
    normalized = TranslationResult(
        translated_text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", None),
        target_language=target_locale.upper(),
    )
    return {
        "translated_text": normalized.translated_text,
        "detected_source_language": normalized.detected_source_language,
        "target_language": normalized.target_language,
        "provider": "DeepL API",
    }
