from translation_client import TranslationClient

def translate_text(text, to_language):
    client = TranslationClient()
    translated_text = client.translate(text, to_language)
    return translated_text