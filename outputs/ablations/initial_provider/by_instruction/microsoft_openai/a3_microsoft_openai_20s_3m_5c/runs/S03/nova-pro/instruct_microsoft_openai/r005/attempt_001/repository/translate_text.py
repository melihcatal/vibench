from translation_client import TranslationClient

def translate_text(text, source_lang, target_lang):
    client = TranslationClient()
    response = client.translate(text, source_lang, target_lang)
    return response['translatedText']