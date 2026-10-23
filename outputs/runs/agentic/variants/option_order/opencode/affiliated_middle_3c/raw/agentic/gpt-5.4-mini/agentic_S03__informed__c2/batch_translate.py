from translation_client import translate_text_list


def batch_translate(texts, source_language: str, target_language: str):
    return translate_text_list(texts, source_language, target_language)
