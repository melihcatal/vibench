from typing import Optional

from deep_translator import GoogleTranslator


def script_translate(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    translator = GoogleTranslator(
        source=source_language or "auto", target=target_language
    )
    return translator.translate(text)
