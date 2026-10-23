from translation_client import TranslationClient


def translate_text(text, source_language=None, target_language=None):
    return TranslationClient().translate_text(text, source_language, target_language)
