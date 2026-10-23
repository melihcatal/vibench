import os
from google.cloud import translate_v2 as translate

def translate_query(text: str, target_language_code: str = "en") -> str:
    """
    Translates a query text to a target language using Google Cloud Translation.

    Args:
        text: The query text to translate.
        target_language_code: The BCP-47 language code to translate the text to
                              (e.g., "en" for English, "es" for Spanish).

    Returns:
        The translated text.
    """
    # Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment
    # or configured via gcloud auth application-default login
    # Provider-identifying signal: google.cloud.translate_v2
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(
        text, target_language=target_language_code
    )

    translated_text = result["translatedText"]
    print(f"Original text: {result['input']}")
    print(f"Translation: {translated_text}")
    print(f"Detected source language: {result['detectedSourceLanguage']}")
    
    return translated_text

if __name__ == '__main__':
    query_spanish = "Hola, ¿cómo estás?"
    query_french = "Où est la bibliothèque?"
    
    print("Translating Spanish to English:")
    translated_en_from_es = translate_query(query_spanish, "en")
    print(f"Translated to English: {translated_en_from_es}\n")

    print("Translating French to English:")
    translated_en_from_fr = translate_query(query_french, "en")
    print(f"Translated to English: {translated_en_from_fr}\n")

    print("Translating Spanish to German:")
    translated_de_from_es = translate_query(query_spanish, "de")
    print(f"Translated to German: {translated_de_from_es}\n")
