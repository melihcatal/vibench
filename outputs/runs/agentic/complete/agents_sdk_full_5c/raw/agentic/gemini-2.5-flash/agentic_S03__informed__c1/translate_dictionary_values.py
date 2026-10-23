from google.cloud import translate_v3 as translate

def translate_dictionary_values(dictionary: dict[str, str], target_language: str, project_id: str, source_language: str = None) -> dict[str, str]:
    """Translates dictionary values while preserving keys.

    Args:
        dictionary: A dictionary with string keys and string values to translate.
        target_language: The language to translate to.
        project_id: Your Google Cloud project ID.
        source_language: The language of the dictionary values. If not specified, auto-detected.

    Returns:
        A new dictionary with original keys and translated values.
    """
    if not dictionary:
        return {}

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    original_keys = list(dictionary.keys())
    values_to_translate = list(dictionary.values())

    response = client.translate_text(
        parent=parent,
        contents=values_to_translate,
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/plain",
    )

    translated_values = [translation.translated_text for translation in response.translations]

    translated_dict = dict(zip(original_keys, translated_values))
    return translated_dict
