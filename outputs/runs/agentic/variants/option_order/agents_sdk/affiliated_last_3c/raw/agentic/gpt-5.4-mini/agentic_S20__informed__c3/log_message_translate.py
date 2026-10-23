from __future__ import annotations

from deepl import Translator

from observability_models import TranslationResult


translator = Translator(auth_key=__import__("os").getenv("DEEPL_AUTH_KEY", ""))


def log_message_translate(text: str, target_locale: str = "fr") -> TranslationResult:
    result = translator.translate_text(text, target_lang=target_locale.upper())
    return TranslationResult(source_text=text, translated_text=str(result), target_locale=target_locale, raw=result)
