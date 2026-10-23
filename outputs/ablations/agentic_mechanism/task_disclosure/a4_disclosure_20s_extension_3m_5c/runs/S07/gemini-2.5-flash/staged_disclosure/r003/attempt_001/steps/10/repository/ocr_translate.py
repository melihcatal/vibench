from google.cloud import translate_v2 as translate
import os

def translate_text(text, target_language='en'):
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The language to translate to (e.g., 'en' for English).

    Returns:
        The translated text.
    """
    # Instantiates a client
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, but we'll assume a single string for this example.
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    
    # Check if GOOGLE_APPLICATION_CREDENTIALS is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your Google Cloud service account key file.")
    else:
        text_to_translate = "Hola, mundo!"
        translated_text = translate_text(text_to_translate, target_language='es')
        print(f"Original text: {text_to_translate}")
        print(f"Translated text (English): {translated_text}")

        text_to_translate_french = "Bonjour le monde!"
        translated_text_spanish = translate_text(text_to_translate_french, target_language='es')
        print(f"Original text: {text_to_translate_french}")
        print(f"Translated text (Spanish): {translated_text_spanish}")
