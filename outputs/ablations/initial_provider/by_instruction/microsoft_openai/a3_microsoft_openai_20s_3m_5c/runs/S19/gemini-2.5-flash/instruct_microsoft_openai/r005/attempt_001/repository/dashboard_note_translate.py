import os
from google.cloud import translate_v2 as translate

def dashboard_note_translate(text: str, target_language: str) -> str:
    # Google Cloud Translation API requires GOOGLE_APPLICATION_CREDENTIALS to be set
    # or explicit client initialization with credentials.
    # Assuming GOOGLE_APPLICATION_CREDENTIALS is set for simplicity in this example.
    translate_client = translate.Client()

    if not text:
        return ""

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        raise RuntimeError(f"Failed to translate text using Google Cloud Translation API: {e}")

if __name__ == "__main__":
    # Example Usage
    # Requires GOOGLE_APPLICATION_CREDENTIALS to be set up for a service account
    # with Translation API permissions.
    text_to_translate = "The server CPU utilization is high."
    target_lang = "es"

    try:
        translated_text = dashboard_note_translate(text_to_translate, target_lang)
        print(f"Original text: {text_to_translate}")
        print(f"Translated ({target_lang}): {translated_text}")
    except Exception as e:
        print(f"Error: {e}")
