from google.cloud import translate_v2 as translate
import os


def appeal_translate(text: str, target_language: str = "en") -> str:
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    try:
        translate_client = translate.Client()
    except Exception as e:
        raise ConnectionError(
            f"Could not initialize Google Cloud Translate client. Ensure GOOGLE_APPLICATION_CREDENTIALS is set. Error: {e}"
        )

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
