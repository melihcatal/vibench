from translation_client import translate_markup_value


def translate_markup(markup: str, target_language: str, source_language: str | None = None) -> str:
    return translate_markup_value(markup, target_language, source_language)
