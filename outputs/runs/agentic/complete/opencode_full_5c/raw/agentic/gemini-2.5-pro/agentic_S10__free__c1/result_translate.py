import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()


def translate_text(text: str, target_language: str) -> str:
    # Google Application Credentials must be set in the environment
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
