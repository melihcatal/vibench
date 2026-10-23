from __future__ import annotations

import os
from typing import Optional

from deepl import Translator

from speech_models import TranslationRequest


DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"


def translate_transcript(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    auth_key = os.getenv(DEEPL_AUTH_KEY_ENV, "").strip()
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    translator = Translator(auth_key)
    request = TranslationRequest(source_text=text, target_language=target_language, source_language=source_language)
    result = translator.translate_text(request.source_text, target_lang=request.target_language, source_lang=request.source_language)
    return result.text
