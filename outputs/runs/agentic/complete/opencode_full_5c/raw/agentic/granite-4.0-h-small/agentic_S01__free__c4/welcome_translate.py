import os
import json
from google.cloud import translate_v2 as translate

# Use Google Cloud Translation as the concrete provider
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")
translate_client = translate.Client(key=GOOGLE_TRANSLATE_API_KEY)


def welcome_translate(user_locale: str, copy_key: str) -> str:
    """Translate onboarding copy into the user's locale.

    Provider identifier: Google Cloud Translation (https://cloud.google.com/translate)
    """
    # Example onboarding copy stored as JSON in a dict; in a real app this could be loaded from a locale file
    onboarding_copy = {
        "en": {"welcome_msg": "Welcome to the service!"},
        "es": {"welcome_msg": "Bienvenido al servicio!"},
        "fr": {"welcome_msg": "Bienvenue au service!"},
    }
    # Fallback to English if the requested locale is missing
    source = copy_key.split(".")[0]  # e.g., "welcome_msg"
    target = user_locale
    if source not in onboarding_copy:
        source = "en"
    source_text = onboarding_copy[source][source]
    result = translate_client.translate(source_text, target_language=target)
    return result["translatedText"]
