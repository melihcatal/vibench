from google.cloud import translate

def translate_dictionary_values(dictionary: dict, target_language: str) -> dict:
    """
    Translates dictionary values while preserving keys using Google Cloud Translation API.

    Args:
        dictionary: A dictionary where values are strings to be translated.
        target_language: The language code to translate the values into (e.g., "en", "es", "fr").

    Returns:
        A new dictionary with the same keys and translated values.
    """
    client = translate.TranslationServiceClient()
    translated_dictionary = {}

    for key, value in dictionary.items():
        if isinstance(value, str):
            response = client.translate_text(
                contents=[value],
                target_language_code=target_language,
                parent=f"projects/YOUR_PROJECT_ID/locations/global"  # Replace YOUR_PROJECT_ID with your actual project ID
            )
            translated_dictionary[key] = response.translations[0].translated_text
        else:
            translated_dictionary[key] = value  # Preserve non-string values
            
    return translated_dictionary
