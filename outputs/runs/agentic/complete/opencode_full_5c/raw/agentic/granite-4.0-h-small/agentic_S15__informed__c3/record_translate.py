# [LATER-STEP] record_translate.py
# Translate user‑facing document fields using DeepL API

import os
import requests
import json

# DeepL API configuration (uses environment variables)
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
TRANSLATE_ENDPOINT = "https://api.deepl.com/v2/translate"


def translate_fields(fields, target_lang="en"):
    """Translate text values in a document to a target language.

    Args:
        fields (dict): Document field/value pairs (strings).
        target_lang (str): DeeL language code (e.g., 'en', 'fr', 'de').

    Returns:
        dict: New dict with translated text for each string value.
    """
    payload = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": [str(value) for value in fields.values()],
        "target_lang": target_lang,
    }
    response = requests.post(TRANSLATE_ENDPOINT, data=payload)
    response.raise_for_status()
    data = response.json()
    translations = data["translations"]
    # Map original fields back to translated text
    translated = {}
    for field, translated_item in zip(fields.keys(), translations):
        translated[field] = translated_item["text"]
    return translated


# Example:
# doc = {'title': 'Bonjour', 'body': 'Ceci est un test.'}
# print(translate_fields(doc, target_lang='en'))
