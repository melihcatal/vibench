import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language="en"):
    """Translates text into the target language."""
    # Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate using a service account key file.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    text_to_translate = "Hola, ¿cómo estás?"
    target_lang = "en"
    translated_text = translate_text(text_to_translate, target_lang)
    print(f"Original text: {text_to_translate}")
    print(f"Translated text ({target_lang}): {translated_text}")

    text_to_translate_french = "Je suis très bien, merci."
    target_lang_spanish = "es"
    translated_text_spanish = translate_text(text_to_translate_french, target_lang_spanish)
    print(f"Original text: {text_to_translate_french}")
    print(f"Translated text ({target_lang_spanish}): {translated_text_spanish}")
