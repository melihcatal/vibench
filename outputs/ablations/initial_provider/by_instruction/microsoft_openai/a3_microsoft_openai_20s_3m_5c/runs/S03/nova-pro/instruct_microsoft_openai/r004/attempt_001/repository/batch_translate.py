from translation_client import TranslationClient

def batch_translate(texts, to_language):
    client = TranslationClient()
    translated_texts = [client.translate(text, to_language) for text in texts]
    return translated_texts