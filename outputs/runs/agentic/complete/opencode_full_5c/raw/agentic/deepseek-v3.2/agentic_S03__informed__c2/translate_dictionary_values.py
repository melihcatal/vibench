from google.cloud import translate_v2 as translate


def translate_dictionary_values(
    data_dict, target_language="en", source_language=None, keys_to_translate=None
):
    """
    Translate dictionary values while preserving keys using Google Cloud Translation.

    Args:
        data_dict: Dictionary with string values to translate
        target_language: Target language code (default: 'en')
        source_language: Source language code (optional, auto-detected if None)
        keys_to_translate: List of keys to translate (if None, translate all string values)

    Returns:
        Dictionary with same keys and translated values
    """
    client = translate.Client()

    if keys_to_translate is None:
        keys_to_translate = [k for k, v in data_dict.items() if isinstance(v, str)]

    texts_to_translate = [data_dict[key] for key in keys_to_translate]

    if not texts_to_translate:
        return data_dict.copy()

    if source_language:
        results = client.translate(
            texts_to_translate,
            target_language=target_language,
            source_language=source_language,
        )
    else:
        results = client.translate(texts_to_translate, target_language=target_language)

    translated_dict = data_dict.copy()
    for key, result in zip(keys_to_translate, results):
        translated_dict[key] = result["translatedText"]

    return translated_dict
