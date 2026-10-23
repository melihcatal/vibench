import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    """
    Translates text into the target language using Google Cloud Translation API.
    
    Requires authentication to be set up, e.g., via the GOOGLE_APPLICATION_CREDENTIALS
    environment variable.
    """
    try:
        translate_client = translate.Client()

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        result = translate_client.translate(text, target_language=target_language)
        
        return result["translatedText"]

    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return f"Translation failed: {e}"


if __name__ == '__main__':
    # This requires `gcloud auth application-default login` to have been run
    # or the GOOGLE_APPLICATION_CREDENTIALS env var to be set.
    try:
        text_to_translate = "Hello, world! This is a test of the translation API."
        target = "es" # Spanish
        
        translation = translate_text(text_to_translate, target)
        
        print(f"Original ('en'): {text_to_translate}")
        print(f"Translated ('{target}'): {translation}")

    except Exception as e:
        print(f"Could not run example. Is Google Cloud authentication configured? Error: {e}")
        print("Try running 'gcloud auth application-default login'")
