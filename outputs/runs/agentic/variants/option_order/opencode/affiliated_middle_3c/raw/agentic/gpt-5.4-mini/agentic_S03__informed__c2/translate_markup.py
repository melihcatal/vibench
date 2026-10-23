from translation_client import translate_html_text


def translate_markup(
    markup_text: str, source_language: str, target_language: str
) -> str:
    return translate_html_text(markup_text, source_language, target_language)
