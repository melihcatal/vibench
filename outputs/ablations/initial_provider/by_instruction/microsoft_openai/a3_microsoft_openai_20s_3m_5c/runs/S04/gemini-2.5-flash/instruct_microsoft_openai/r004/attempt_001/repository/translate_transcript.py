from google.cloud import translate_v2 as translate
import os

def translate_text(text: str, target_language: str) -> str:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_TRANSLATION_CREDENTIALS_PATH")
    if not os.environ.get("GOOGLE_TRANSLATION_CREDENTIALS_PATH"):
        raise ValueError("GOOGLE_TRANSLATION_CREDENTIALS_PATH environment variable must be set.")

    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
