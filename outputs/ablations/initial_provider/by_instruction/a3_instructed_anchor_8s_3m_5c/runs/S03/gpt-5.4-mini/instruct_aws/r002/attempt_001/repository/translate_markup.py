from translation_client import TranslationClient


def translate_markup(markup, source_language=None, target_language="en", region_name=None):
    client = TranslationClient(region_name=region_name)
    return client.translate_markup(markup, source_language, target_language)
