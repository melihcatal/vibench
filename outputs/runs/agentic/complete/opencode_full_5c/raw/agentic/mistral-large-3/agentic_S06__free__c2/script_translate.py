from google.cloud import translate_v2 as translate
import os


def translate_script(text: str, target_language: str) -> str:
    client = translate.Client()

    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
