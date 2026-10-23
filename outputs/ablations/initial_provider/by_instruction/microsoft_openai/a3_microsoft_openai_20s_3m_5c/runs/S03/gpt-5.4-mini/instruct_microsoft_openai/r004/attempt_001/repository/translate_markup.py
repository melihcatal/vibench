from translate_text import translate_text


def translate_markup(markup: str, source_language=None, target_language="en"):
    return translate_text(markup, source_language=source_language, target_language=target_language).translated_text
