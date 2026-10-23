# [SAME-SCENARIO] translate_text.py

import os
from google.cloud import translate_v2 as translate

# Use Google Cloud Translation as the concrete provider
# Provider identification: google-cloud-translate SDK import and GOOGLE_APPLICATION_CREDENTIALS env variable


def translate_text(source_text: str, target_language: str = "es") -> str:
    """Translate a single text string using Google Cloud Translation.

    Args:
        source_text (str): The text to translate.
        target_language (str): Target language code (default: "es").

    Returns:
        str: Translated text.
    """
    # Initialize client using default credentials
    client = translate.Client()
    result = client.translate(source_text, target_language=target_language)
    return result["translatedText"]


# Example usage (guarded by __main__ check)
if __name__ == "__main__":
    sample = "Hello, world!"
    print(f"Original: {sample}")
    print(f"Translated: {translate_text(sample)}")
