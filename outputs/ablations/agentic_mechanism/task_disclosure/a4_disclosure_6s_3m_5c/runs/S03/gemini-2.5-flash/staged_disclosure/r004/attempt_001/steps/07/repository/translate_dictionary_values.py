import os
from google.cloud import translate_v3beta1

def translate_dictionary_values(input_dict, target_language):
    """
    Translates the values of a dictionary to a specified target language,
    preserving the original keys.

    Args:
        input_dict (dict): The dictionary whose values are to be translated.
        target_language (str): The language code to translate to (e.g., "es" for Spanish).

    Returns:
        dict: A new dictionary with the translated values.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate_v3beta1.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    translated_dict = {}

    for key, value in input_dict.items():
        if isinstance(value, str):
            response = client.translate_text(
                parent=parent,
                contents=[value],
                target_language_code=target_language,
            )
            for translation in response.translations:
                translated_dict[key] = translation.translated_text
        else:
            translated_dict[key] = value  # Preserve non-string values
    return translated_dict

if __name__ == "__main__":
    # Example Usage:
    my_dict = {
        "hello": "Hello, world!",
        "greeting": "How are you?",
        "number": 123,
        "list": ["item1", "item2"],
    }
    target_lang = "es"

    print(f"Original dictionary: {my_dict}")
    try:
        translated_dict = translate_dictionary_values(my_dict, target_lang)
        print(f"Translated dictionary (to {target_lang}): {translated_dict}")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable and ensure authentication is configured.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
