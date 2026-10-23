from translation_client import TranslationClient


def translate_dictionary_values(values, source_language=None, target_language="en", region_name=None):
    client = TranslationClient(region_name=region_name)
    return client.translate_dictionary_values(values, source_language, target_language)
