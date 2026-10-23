from google.cloud import translate_v2 as translate
import os

def welcome_translate(text, target_language):
    # Instantiates a client
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Translate the text
    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']
