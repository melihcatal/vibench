import os
from google.cloud import translate_v2 as translate

def translate_dictionary_values(dictionary: dict, target_language: str, source_language: str = None) -> dict:
    """Translates dictionary values while preserving keys using Google Cloud Translation."""
    client = translate.Client()
    translated_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, str):
            result = client.translate(
                value,
                target_language=target_language,
                source_language=source_language,
                model='nmt' # Neural Machine Translation model
            )
            translated_dict[key] = result['translatedText']
        else:
            translated_dict[key] = value
    return translated_dict

if __name__ == '__main__':
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    my_dict = {"greeting": "Hello", "farewell": "Goodbye", "number": 123}
    translated_dict = translate_dictionary_values(my_dict, "it")
    print(f"Translated dictionary: {translated_dict}")
