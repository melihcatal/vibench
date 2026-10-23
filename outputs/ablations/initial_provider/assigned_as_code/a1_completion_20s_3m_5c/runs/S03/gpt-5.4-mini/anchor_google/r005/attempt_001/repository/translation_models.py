def normalize_translation_result(translation, source_language, target_language):
    return {
        "text": translation.translated_text,
        "source_language": source_language,
        "target_language": target_language,
    }
