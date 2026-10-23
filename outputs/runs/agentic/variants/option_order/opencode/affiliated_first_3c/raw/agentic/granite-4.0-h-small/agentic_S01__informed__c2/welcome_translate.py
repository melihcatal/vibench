import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation configuration (use env vars in deployment)
TRANSLATOR = translate.Client()


def welcome_translate(user_locale: str, onboarding_payload: dict) -> dict:
    """Translate onboarding copy into the user's locale using Google Cloud Translation.

    Args:
        user_locale: BCP-47 language tag, e.g. 'es', 'fr', 'zh-Hans'.
        onboarding_payload: dictionary containing fields like 'welcome_message', 'instructions', etc.

    Returns a new dict with translated versions of each string field.
    """
    translated = {}
    for key, value in onboarding_payload.items():
        # Detect source language automatically; you can also pass src_lang if known
        result = TRANSLATOR.translate(value, target_language=user_locale)
        translated[key] = result["translatedText"]
    return translated
