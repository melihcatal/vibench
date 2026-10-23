import os
from google.cloud import translate_v2 as translate


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    """
    Translate appeal text for review using Google Cloud Translation.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS_PATH"
    )  # Assuming path to credentials file
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
