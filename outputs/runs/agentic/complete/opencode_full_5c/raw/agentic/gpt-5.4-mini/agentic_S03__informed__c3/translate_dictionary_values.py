from translation_client import TranslationClient


def translate_dictionary_values(values, source_language=None, target_language=None):
    return TranslationClient().translate_mapping_values(values, source_language, target_language)
