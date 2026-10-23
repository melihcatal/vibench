import os
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str) -> str:
    """Translates text into the target language using Google Cloud Translation."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication.
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]


if __name__ == "__main__":
    # Example usage
    # translated_text = translate_text("Hello, world!", "es")
    # print(f"Translated text: {translated_text}")
    pass
