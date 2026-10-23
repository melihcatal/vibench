from google.cloud import translate_v2 as translate
import os


def payload_translate(text: str, target_language: str = "es") -> str:
    """
    Translates customer-facing message payload text.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
        )

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
