from translation_client import translate_text as _translate_text


def translate_text(text, source_language, target_language):
    return _translate_text(text, source_language, target_language)
