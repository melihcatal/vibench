
from google.cloud import translate_v2 as translate
import os

def translate_caption(text, target_language="es"):
    """Translates text into the target language using Google Cloud Translation."""
    # Instantiates a client
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of translations for each text.
    result = translate_client.translate(text, target_language=target_language)

    # print(f"Text: {result['input']}")
    # print(f"Translation: {result['translatedText']}")
    # print(f"Detected source language: {result['detectedSourceLanguage']}")
    return result["translatedText"]

if __name__ == "__main__":
    # This is a placeholder for live caption input.
    # In a real application, you would integrate with a live captioning system
    # to receive text in real-time.
    live_caption_text = "Hello, how are you doing today?"
    target_language = "fr" # French

    translated_text = translate_caption(live_caption_text, target_language)
    print(f"Original Caption: {live_caption_text}")
    print(f"Translated Caption ({target_language}): {translated_text}")

    live_caption_text_2 = "Nice to meet you."
    target_language_2 = "de" # German
    translated_text_2 = translate_caption(live_caption_text_2, target_language_2)
    print(f"Original Caption: {live_caption_text_2}")
    print(f"Translated Caption ({target_language_2}): {translated_text_2}")
