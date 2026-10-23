import os
from google.cloud import translate_v2 as translate


def translate_payload(text: str, target_language: str) -> str:
    """Translates customer-facing message payload text."""
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]


if __name__ == "__main__":
    # This requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    sample_text = "Hello, this is a test message for translation."
    target = "es"  # Spanish
    translated_text = translate_payload(sample_text, target)
    print(f"Original: {sample_text}")
    print(f"Translated ({target}): {translated_text}")
