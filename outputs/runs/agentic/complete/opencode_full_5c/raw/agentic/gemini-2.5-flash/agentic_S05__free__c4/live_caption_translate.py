import os

from google.cloud import translate_v2 as translate


def translate_caption(text: str, target_language: str = "es") -> str:
    """Translates a given text into the target language using Google Cloud Translation."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set for Translation."
        )

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a list of translated texts.
    result = translate_client.translate(text, target_language=target_language)

    # print(f"Text: {result['input']}")
    # print(f"Translation: {result['translatedText']}")
    # print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result["translatedText"]
