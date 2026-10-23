import os
from typing import Dict

# Import the appropriate SDK for the provider. Here we use Google Cloud Translation as the concrete provider.
from google.cloud import translate_v2 as translate

# Configuration using environment variable for credentials
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def translate_dictionary_values(data: Dict[str, str], source_lang: str = "en", target_lang: str = "es") -> Dict[str, str]:
    """Translate dictionary values while preserving keys.
    Uses Google Cloud Translation SDK.
    """
    client = translate.Client()
    translated = {}
    for key, value in data.items():
        result = client.translate(value, source_language=source_lang, target_language=target_lang)
        translated[key] = result["translatedText"]
    return translated
