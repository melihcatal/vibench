from translation_client import translate_text_value


def translate_text(text: str, target_language: str, source_language: str | None = None) -> str:
    return translate_text_value(text, target_language, source_language)
