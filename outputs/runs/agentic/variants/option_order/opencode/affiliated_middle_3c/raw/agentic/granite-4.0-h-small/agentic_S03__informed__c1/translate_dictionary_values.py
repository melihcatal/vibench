def translate_dictionary_values(
    data: dict, source_lang: str = "en", target_lang: str = "es"
) -> dict:
    """Translate dictionary values while preserving keys.

    This helper assumes string values. Nested dictionaries are not traversed.
    """
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = translate_text(value, source_lang, target_lang)
        else:
            translated[key] = value  # Non-string values are kept unchanged
    return translated
