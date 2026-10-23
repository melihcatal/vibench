from translation_client import TranslationClient

def translate_markup(markup, to_language):
    client = TranslationClient()
    translated_markup = client.translate(markup, to_language)
    return translated_markup