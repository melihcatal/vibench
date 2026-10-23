# [LATER-STEP] script_translate.py

import os
from google.cloud import translate_v2 as translate

# Load credentials (env var GOOGLE_APPLICATION_CREDENTIALS required)
client = translate.Client()


def translate_script(script: str, target_language: str = "es") -> str:
    """Translates a narration script to the target language.

    Args:
        script: Original narration text.
        target_language: ISO-639-1 code (e.g., "es" for Spanish).

    Returns:
        Translated script text.
    """
    result = client.translate(script, target_language=target_language)
    return result["translatedText"]


# Example usage (uncomment to test):
# print(translate_script("Hello, world!", "fr"))
