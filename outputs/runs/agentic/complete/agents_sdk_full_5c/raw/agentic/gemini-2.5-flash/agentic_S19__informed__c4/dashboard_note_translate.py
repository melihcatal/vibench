from google.cloud import translate_v2 as translate
import os

def translate_dashboard_note(text: str, target_language: str):
    # Google Cloud Translation automatically uses credentials from GOOGLE_APPLICATION_CREDENTIALS
    # or other standard Google Cloud authentication methods.
    client = translate.Client()
    
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language)

    # The result is a dictionary; "translatedText" contains the translated string.
    return result["translatedText"]

