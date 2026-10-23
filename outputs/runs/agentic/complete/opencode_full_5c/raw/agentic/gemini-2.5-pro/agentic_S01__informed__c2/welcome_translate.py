import os
from google.cloud import translate_v2 as translate


def translate_welcome_message(text: str, target_language: str) -> str:
    """Translates text into the target language."""
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]


# Example usage for local testing (requires GOOGLE_APPLICATION_CREDENTIALS)
# if __name__ == '__main__':
#     translated = translate_welcome_message("Hello, welcome to our service!", "fr")
#     print(translated)
