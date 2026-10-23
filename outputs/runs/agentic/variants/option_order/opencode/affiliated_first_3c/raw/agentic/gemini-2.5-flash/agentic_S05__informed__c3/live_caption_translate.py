from google.cloud import translate_v2 as translate
import os


def translate_caption(text: str, target_language: str = "es"):
    client = translate.Client()
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is used for authentication.
    # The client automatically picks up the credentials.
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
