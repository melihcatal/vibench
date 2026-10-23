import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()

def translate_text(text: str, target_language: str = "es") -> str:
    """
    Translates text using Google Cloud Translation API.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    or authenticated through `gcloud auth application-default login`.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    # To run this example, ensure you have Google Cloud credentials configured.
    # For instance, set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # to the path of your service account key file.
    # You can also authenticate using `gcloud auth application-default login`
    
    # original_text = "Hello, how are you today? This is a test for translation."
    # translated_text = translate_text(original_text, target_language="fr")
    # print(f"Original: {original_text}")
    # print(f"Translated (French): {translated_text}")

    # translated_text_es = translate_text(original_text, target_language="es")
    # print(f"Translated (Spanish): {translated_text_es}")
    pass
