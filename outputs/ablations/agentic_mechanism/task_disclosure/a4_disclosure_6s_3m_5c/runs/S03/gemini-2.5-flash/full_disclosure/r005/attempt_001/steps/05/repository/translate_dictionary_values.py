from google.cloud import translate_v3


def translate_dictionary_values(
    dictionary: dict,
    target_language: str,
    project_id: str,
    source_language: str = None,
) -> dict:
    """Translates the values of a dictionary while preserving its keys.

    Args:
        dictionary: A dictionary with string values to be translated.
        target_language: The language to translate the values into (e.g., "en-US").
        project_id: The ID of the Google Cloud project.
        source_language: The language of the source text (e.g., "es"). If not
                         specified, the API will attempt to detect the language.

    Returns:
        A new dictionary with the same keys and translated values.
    """
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    translated_dictionary = {}
    for key, value in dictionary.items():
        if not isinstance(value, str):
            translated_dictionary[key] = value
            continue

        config = translate_v3.TranslateTextRequest.SingleTranslationConfig(
            source_language_code=source_language,
            target_language_code=target_language,
        )

        request = translate_v3.TranslateTextRequest(
            parent=parent,
            contents=[value],
            single_translation_config=config,
        )

        response = client.translate_text(request=request)
        translated_dictionary[key] = response.translations[0].translated_text

    return translated_dictionary
