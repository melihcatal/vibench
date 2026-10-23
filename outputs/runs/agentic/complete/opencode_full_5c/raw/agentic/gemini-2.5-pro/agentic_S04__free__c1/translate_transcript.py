from google.cloud import translate_v2 as translate
import os


def translate_transcript(text: str, target_language: str = "es") -> str:
    """
    Translates completed transcript segments using Google Cloud Translate.
    """
    os.environ.setdefault(
        "GOOGLE_APPLICATION_CREDENTIALS", os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
