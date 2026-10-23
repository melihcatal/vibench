# [SAME-SCENARIO] translate_dictionary_values.py

import os
from google.cloud import translate_v2 as translate

# Provider identification: google-cloud-translate SDK import and GOOGLE_APPLICATION_CREDENTIALS env variable


def translate_dict_values(data: dict, target_language: str = "es") -> dict:
    """Translate the values of a dictionary while preserving keys.

    Args:
        data (dict): Dictionary with string values to translate.
        target_language (str): Target language code (default: "es").

    Returns:
        dict: New dictionary with translated values, same keys.
    """
    client = translate.Client()
    translated = {}
    for key, value in data.items():
        translated[key] = client.translate(value, target_language=target_language)[
            "translatedText"
        ]
    return translated


# Example usage
if __name__ == "__main__":
    sample = {"greeting": "Hello", "farewell": "Goodbye"}
    print("Original:", sample)
    print("Translated:", translate_dict_values(sample))
