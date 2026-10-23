from google.cloud import translate

def translate_dictionary_values(input_dict: dict, target_language: str, project_id: str, source_language: str = None) -> dict:
    """
    Translates the values of a dictionary while preserving its keys using Google Cloud Translation.

    Args:
        input_dict: A dictionary where values are strings to be translated.
        target_language: The language code to translate the values into (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.
        source_language: The language code of the input text (e.g., "en" for English).
                         If not specified, Google Cloud Translation will auto-detect.

    Returns:
        A new dictionary with translated values, preserving the original keys.
    """
    translate_client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    translated_dict = {}

    for key, value in input_dict.items():
        if isinstance(value, str):
            request = {
                "parent": parent,
                "contents": [value],
                "target_language_code": target_language,
            }
            if source_language:
                request["source_language_code"] = source_language

            response = translate_client.translate_text(request=request)
            translated_dict[key] = response.translations[0].translated_text
        else:
            translated_dict[key] = value  # Preserve non-string values as is
            
    return translated_dict
