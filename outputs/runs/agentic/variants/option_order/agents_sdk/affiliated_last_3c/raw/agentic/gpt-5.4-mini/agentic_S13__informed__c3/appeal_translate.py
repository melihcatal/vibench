from __future__ import annotations

from deepl import Translator

from safety_models import TranslationRequest


def translate_appeal(text: str, target_language: str = "EN") -> str:
    req = TranslationRequest(text=text, target_language=target_language)
    translator = Translator(auth_key="")
    result = translator.translate_text(req.text, target_lang=req.target_language)
    return result.text
