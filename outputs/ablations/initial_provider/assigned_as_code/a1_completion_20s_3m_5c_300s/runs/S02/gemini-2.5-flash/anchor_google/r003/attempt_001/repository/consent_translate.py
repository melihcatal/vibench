import os
from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language: str = "en") -> str:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PATH")
    translate_client = translate.Client()

    response = translate_client.translate(text, target_language=target_language)
    return response["translatedText"]
