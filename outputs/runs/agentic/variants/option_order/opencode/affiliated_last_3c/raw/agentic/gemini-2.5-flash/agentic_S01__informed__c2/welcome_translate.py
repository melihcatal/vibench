import os
from google.cloud import translate_v2 as translate


def welcome_translate(text: str, target_language: str) -> str:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS", "path/to/your/credentials.json"
    )  # Placeholder
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
