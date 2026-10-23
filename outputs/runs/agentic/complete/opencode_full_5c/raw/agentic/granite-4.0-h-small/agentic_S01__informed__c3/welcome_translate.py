# welcome_translate.py
# Translate onboarding copy into the user's locale (later-step integration)

import os
from typing import Optional
from google.cloud.translate_v2 import Client as TranslateClient

# Configure concrete provider: Google Cloud Translation
GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS", "service_account.json"
)

translate_client = TranslateClient()


def translate_welcome(text: str, target_lang: Optional[str] = None) -> str:
    """
    Translate onboarding welcome text to the specified locale.
    If target_lang is None, uses the default target set in env var TARGET_LANG.
    """
    lang = target_lang or os.getenv("TARGET_LANG", "en")
    result = translate_client.translate(text, target_language=lang)
    return result["translatedText"]


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(translate_welcome("Welcome to our service!", target_lang="es"))
