from translate_text import translate_text
from translation_models import TranslationResult, normalize_text_list


def batch_translate(texts, source_language=None, target_language="en"):
    normalized = normalize_text_list(texts)
    return [TranslationResult(translated_text=translate_text(text, source_language, target_language).translated_text, source_language=source_language, target_language=target_language) for text in normalized]
