import os
from google.cloud import translate_v2 as translate


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    client = translate.Client()
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication

    response = client.translate(text, target_language=target_language)
    return response["translatedText"]
