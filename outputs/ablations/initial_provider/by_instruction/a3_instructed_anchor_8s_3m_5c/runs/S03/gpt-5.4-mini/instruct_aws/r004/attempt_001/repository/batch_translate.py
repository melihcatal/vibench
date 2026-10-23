from translation_client import translate_texts as _translate_texts


def batch_translate(texts, source_language, target_language):
    return _translate_texts(texts, source_language, target_language)
