from translation_client import translate_texts


def batch_translate(texts, source_language: str, target_language: str):
    response = translate_texts(texts, source_language, target_language)
    return response.translated_texts
