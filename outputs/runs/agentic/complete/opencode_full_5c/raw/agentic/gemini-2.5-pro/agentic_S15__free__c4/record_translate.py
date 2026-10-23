import os
from google.cloud import translate_v2 as translate


def record_translate(text: str, target_language: str):
    """Translates text into the target language."""
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set."
        )

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(
        text, target_language=target_language, model="nmt"
    )

    return result["translatedText"]
