
from google.cloud import translate_v2 as translate
import os

def translate_text(text, target_language="en"):
    """Translates text into the target language using Google Cloud Translation."""
    # Instantiates a client
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Google Cloud Translation API can only translate plaintext.
    result = translate_client.translate(text, target_language=target_language)

    # The Google Cloud Translation API is identifiable through the client library
    # and the specific API call being made.

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage (replace with your actual image description)
    text_to_translate = "Une belle image d'un chat jouant avec une balle."
    target_lang = "en"
    translated_description = translate_text(text_to_translate, target_lang)
    print(f"Original text: {text_to_translate}")
    print(f"Translated text ({target_lang}): {translated_description}")

    text_to_translate_2 = "A happy dog running in a field."
    target_lang_2 = "fr"
    translated_description_2 = translate_text(text_to_translate_2, target_lang_2)
    print(f"Original text: {text_to_translate_2}")
    print(f"Translated text ({target_lang_2}): {translated_description_2}")
