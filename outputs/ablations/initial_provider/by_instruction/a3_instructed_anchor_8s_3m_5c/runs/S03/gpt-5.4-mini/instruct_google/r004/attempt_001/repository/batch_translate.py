from translation_client import translate_texts_value


def batch_translate(texts: list[str], target_language: str, source_language: str | None = None) -> list[str]:
    return translate_texts_value(texts, target_language, source_language)
