# welcome_translate.py

import os
from typing import Any

# Choose a concrete provider; example using Google Cloud Translation
from google.cloud import translate_v2 as translate

# Load credentials from env
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


async def translate_welcome(text: str, target_locale: str = "en") -> Any:
    """Translate onboarding copy into the user's locale using Google Cloud Translation.

    Returns the translated text.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_locale)
    return result["translatedText"]
