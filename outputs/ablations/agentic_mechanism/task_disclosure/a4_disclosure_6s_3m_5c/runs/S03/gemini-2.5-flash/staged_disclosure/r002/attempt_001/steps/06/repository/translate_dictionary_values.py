from google.cloud import translate_v2 as translate

def translate_dictionary_values(input_dict, target_language, source_language=None):
    """
    Translates the values of a dictionary using Google Cloud Translation API while preserving keys.

    Args:
        input_dict (dict): The dictionary whose values are to be translated.
        target_language (str): The BCP-47 language code of the target language (e.g., "fr" for French).
        source_language (str, optional): The BCP-47 language code of the source language.
                                         If not provided, the API will attempt to detect the language.

    Returns:
        dict: A new dictionary with the same keys and translated values.
    """
    translate_client = translate.Client()
    translated_dict = {}

    for key, value in input_dict.items():
        if isinstance(value, str):
            if source_language:
                result = translate_client.translate(value, target_language=target_language, source_language=source_language)
            else:
                result = translate_client.translate(value, target_language=target_language)
            translated_dict[key] = result['translatedText']
        else:
            translated_dict[key] = value  # Preserve non-string values
    return translated_dict

if __name__ == "__main__":
    # Example usage:
    my_dict = {
        "greeting": "Hello World",
        "question": "How are you?",
        "number": 123,
        "list_of_words": ["apple", "banana"]
    }

    # Ensure you have authenticated for Google Cloud Translation API
    # For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Translate to Spanish
    spanish_dict = translate_dictionary_values(my_dict, target_language="es")
    print("Original Dictionary:", my_dict)
    print("Translated to Spanish:", spanish_dict)

    print("-" * 30)

    # Translate to French, explicitly specifying source language as English
    french_dict = translate_dictionary_values(my_dict, target_language="fr", source_language="en")
    print("Original Dictionary:", my_dict)
    print("Translated to French (from English):", french_dict)
