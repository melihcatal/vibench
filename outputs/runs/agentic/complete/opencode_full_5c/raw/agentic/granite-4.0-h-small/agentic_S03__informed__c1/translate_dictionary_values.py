from translate_text import translate_text


def translate_dictionary_values(
    data: dict, src_lang: str = GOOGLE_SOURCE_LANG, tgt_lang: str = GOOGLE_TARGET_LANG
) -> dict:
    """
    Translates all string values in a dictionary while preserving keys.

    Args:
        data: Dictionary with string values to translate.
        src_lang: Source language code.
        tgt_lang: Target language code.

    Returns:
        New dictionary with translated values.
    """
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = translate_text(value, src_lang, tgt_lang)
        elif isinstance(value, dict):
            # Recursively translate nested dictionaries
            translated[key] = translate_dictionary_values(value, src_lang, tgt_lang)
        else:
            translated[key] = value  # non-string values left unchanged
    return translated
