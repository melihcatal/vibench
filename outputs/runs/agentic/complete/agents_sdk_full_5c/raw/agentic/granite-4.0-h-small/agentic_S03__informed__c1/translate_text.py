import os
from typing import List

# Import the appropriate SDK for the provider. Here we use Google Cloud Translation as the concrete provider.
from google.cloud import translate_v2 as translate

# Configuration using environment variable for credentials
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def translate_text(text: str, source_lang: str = "en", target_lang: str = "es") -> str:
    """Translate a single text string between languages.
    Uses Google Cloud Translation SDK.
    """
    client = translate.Client()
    result = client.translate(text, source_language=source_lang, target_language=target_lang)
    return result["translatedText"]

def batch_translate(texts: List[str], source_lang: str = "en", target_lang: str = "es") -> List[str]:
    """Translate a list of strings while preserving order.
    Leverages Google Cloud Translation batch API.
    """
    client = translate.Client()
    responses = client.translate(texts, source_language=source_lang, target_language=target_lang)
    return [r["translatedText"] for r in responses]

def translate_markup(markup_text: str, source_lang: str = "en", target_lang: str = "es") -> str:
    """Translate HTML or markup while preserving tags.
    The Google Translation API automatically wraps tags, so we simply translate the raw text.
    """
    client = translate.Client()
    result = client.translate(markup_text, source_language=source_lang, target_language=target_lang)
    return result["translatedText"]

def translate_dictionary_values(data: dict, source_lang: str = "en", target_lang: str = "es") -> dict:
    """Translate dictionary values while preserving keys.
    """
    client = translate.Client()
    translated = {}
    for key, value in data.items():
        translated[key] = client.translate(value, source_language=source_lang, target_language=target_lang)["translatedText"]
    return translated
