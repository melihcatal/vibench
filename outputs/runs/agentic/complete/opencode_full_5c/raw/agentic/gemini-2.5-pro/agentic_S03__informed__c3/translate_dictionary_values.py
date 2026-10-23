from batch_translate import batch_translate


def translate_dictionary_values(
    data: dict[str, str], target_language: str, source_language: str = "en"
) -> dict[str, str]:
    """
    Translates the string values of a dictionary.

    Args:
        data: A dictionary with string keys and string values to be translated.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        A new dictionary with the same keys but translated values.
    """
    if not data:
        return {}

    keys = list(data.keys())
    values = list(data.values())

    translated_values = batch_translate(values, target_language, source_language)

    return dict(zip(keys, translated_values))
