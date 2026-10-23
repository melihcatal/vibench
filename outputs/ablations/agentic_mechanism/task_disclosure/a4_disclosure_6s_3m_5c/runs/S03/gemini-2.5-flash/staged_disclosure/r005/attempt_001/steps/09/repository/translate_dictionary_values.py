
from google.cloud import translate_v2 as translate

def translate_dictionary_values(input_dict, target_language):
    """
    Translates the values of a dictionary to a target language while preserving keys.

    Args:
        input_dict (dict): The dictionary whose values need to be translated.
        target_language (str): The language code to translate to (e.g., 'es' for Spanish).

    Returns:
        dict: A new dictionary with the translated values and original keys.
    """
    translate_client = translate.Client()
    translated_dict = {}

    for key, value in input_dict.items():
        if isinstance(value, str):
            result = translate_client.translate(value, target_language=target_language)
            translated_dict[key] = result['translatedText']
        else:
            translated_dict[key] = value  # Keep non-string values as they are
    return translated_dict

if __name__ == '__main__':
    # Example usage:
    my_dict = {
        "hello": "Hello, world!",
        "greeting": "How are you?",
        "number": 123,
        "list_of_words": ["apple", "banana"]
    }
    target_lang = "es"  # Spanish

    translated_result = translate_dictionary_values(my_dict, target_lang)
    print(f"Original dictionary: {my_dict}")
    print(f"Translated dictionary (to {target_lang}): {translated_result}")
