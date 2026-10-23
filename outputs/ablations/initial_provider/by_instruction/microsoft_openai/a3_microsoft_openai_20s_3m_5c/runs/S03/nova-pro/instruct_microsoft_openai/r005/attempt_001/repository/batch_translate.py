from translation_client import TranslationClient

def batch_translate(texts, source_lang, target_lang):
    client = TranslationClient()
    translated_texts = []
    for text in texts:
        response = client.translate(text, source_lang, target_lang)
        translated_texts.append(response['translatedText'])
    return translated_texts