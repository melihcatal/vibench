def normalize_text(value):
    return '' if value is None else str(value)


def normalize_strings(values):
    return [normalize_text(value) for value in values]


def build_translation_result(text, source_language, target_language):
    return {
        'text': text,
        'source_language': source_language,
        'target_language': target_language,
    }
