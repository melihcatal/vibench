import os
from translate_client import TranslateClient
from identity_models import RegisterRequest

def welcome_translate(user_email: str, user_locale: str) -> str:
    """Translate onboarding email copy for new users."""
    client = TranslateClient()
    # Example onboarding copy (could be loaded from i18n files)
    source_text = (
        "Welcome to our service, {}!\n\nWe're excited to have you on board.\n\nBest regards,\nYour Team"
    ).format(user_email)
    translated = client.translate(source_text, target_language=user_locale)
    return translated
