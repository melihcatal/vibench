import os
from google.cloud import translate_v2 as translate

def translate_text_content(text: str, target_language: str = "en") -> dict:
    """
    Translates a given text into the target language using Google Cloud Translation API.

    :param text: The text to translate.
    :param target_language: The ISO 639-1 code for the target language.
    :return: A dictionary containing the translation results.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    print(f"Text: {result['input']}")
    print(f"Translation: {result['translatedText']}")
    print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result
