import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate

from translation_client import get_translate_client
from translation_models import BatchTranslationRequest, TranslationResponse

def translate_dictionary_values(dictionary: Dict[str, str], target_language: str, source_language: str = None) -> Dict[str, str]:
    """Translates dictionary values using Google Cloud Translation while preserving keys."""
    client = get_translate_client()

    keys = list(dictionary.keys())
    values_to_translate = list(dictionary.values())

    if not values_to_translate:
        return {}
    
    # Google Cloud Translate API can translate multiple texts in one call
    results = client.translate(
        values_to_translate,
        target_language=target_language,
        source_language=source_language,
        format='text' # Assuming dictionary values are plain text
    )

    translated_dict = {}
    for i, key in enumerate(keys):
        translated_dict[key] = results[i]['translatedText']
    
    return translated_dict

if __name__ == '__main__':
    # Example usage for testing
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/your/google_credentials.json' # Replace with actual path

    my_dict = {
        "greeting": "Hello, world!",
        "farewell": "Good bye, everyone!",
        "question": "How are you?"
    }
    target_lang = "es"

    translated_dict = translate_dictionary_values(my_dict, target_lang)
    print("Original dictionary:", my_dict)
    print(f"Translated dictionary (to {target_lang}):", translated_dict)

    # Example with an empty dictionary
    empty_dict = {}
    translated_empty_dict = translate_dictionary_values(empty_dict, "fr")
    print("Original empty dictionary:", empty_dict)
    print(f"Translated empty dictionary (to fr):", translated_empty_dict)
