from translation_client import translate_many_texts


def batch_translate(texts, source_language: str, target_language: str):
    return translate_many_texts(list(texts), source_language, target_language)
