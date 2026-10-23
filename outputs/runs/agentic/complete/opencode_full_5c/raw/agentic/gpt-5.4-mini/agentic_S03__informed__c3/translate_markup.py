from translation_client import TranslationClient


def translate_markup(markup, source_language=None, target_language=None):
    return TranslationClient().translate_html(markup, source_language, target_language)
