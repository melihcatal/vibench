import os
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates text to the target language using Google Cloud Translation API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # The Python client library for the Translate API uses API keys for authentication.
        raise ValueError(
            "GOOGLE_API_KEY environment variable not set for Translate API."
        )

    translate_client = translate.Client(target_language=target_language)

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
