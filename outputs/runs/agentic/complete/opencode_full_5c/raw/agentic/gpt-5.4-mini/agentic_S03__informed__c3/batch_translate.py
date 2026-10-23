from translation_client import TranslationClient


def batch_translate(texts, source_language=None, target_language=None):
    return TranslationClient().translate_texts(texts, source_language, target_language)
