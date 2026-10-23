from google.cloud import translate

def translate_dictionary_values(input_dict: dict, target_language: str) -> dict:
    """
    Translates dictionary values while preserving keys using Google Cloud Translation API.

    Args:
        input_dict: A dictionary where values are strings to be translated.
        target_language: The target language for translation (e.g., "es" for Spanish).

    Returns:
        A new dictionary with the same keys and translated values.
    """
    client = translate.TranslationServiceClient()
    project_id = "[YOUR_PROJECT_ID]"  # Replace with your Google Cloud Project ID
    location = "global"  # Or your specific region

    translated_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, str):
            parent = f"projects/{project_id}/locations/{location}"
            response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": [value],
                    "target_language_code": target_language,
                }
            )
            translated_dict[key] = response.translations[0].translated_text
        else:
            translated_dict[key] = value
    return translated_dict
