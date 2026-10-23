import os
from typing import Optional

# Example: use a managed translation API such as Google Cloud Translation
# Credentials are loaded from environment variables or secret manager
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

from google.cloud import translate_v2 as translate

client = translate.Client()

def translate_onboarding_copy(text: str, target_locale: str = "en") -> str:
    """Translate onboarding copy into the user's locale using a managed translation service.
    """
    result = client.translate(text, target_language=target_locale)
    return result["translatedText"]