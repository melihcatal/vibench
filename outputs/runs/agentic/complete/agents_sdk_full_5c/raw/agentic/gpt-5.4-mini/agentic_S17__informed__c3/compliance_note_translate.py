from __future__ import annotations

from deepl import Translator

from security_models import TranslationResult

PROVIDER = "DeepL"


def translate_compliance_note(text: str, target_lang: str = "EN-US", auth_key: str | None = None) -> TranslationResult:
    translator = Translator(auth_key or "")
    result = translator.translate_text(text, target_lang=target_lang)
    translated_text = result.text if hasattr(result, "text") else str(result)
    source_lang = getattr(result, "detected_source_lang", None)
    return TranslationResult(
        source_text=text,
        translated_text=translated_text,
        source_lang=source_lang,
        target_lang=target_lang,
        provider=PROVIDER,
    )
