from translation_client import TranslationClient


def batch_translate(texts, source_language=None, target_language="en", region_name=None):
    client = TranslationClient(region_name=region_name)
    return client.batch_translate_text(texts, source_language, target_language)
