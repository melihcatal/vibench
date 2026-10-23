import os
from google.cloud import translate_v2 as translate
from identity_models import RegisterUserResponse

# Initialize Google Cloud Translation client
translate_client = translate.Client.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)


def translate_welcome_message(text: str, target_language: str) -> str:
    """Translate onboarding copy using Google Cloud Translation API."""
    result = translate_client.translate(
        text,
        target_language=target_language,
        model="nmt"  # Neural Machine Translation model
    )
    return result["translatedText"]


def get_localized_welcome(user_locale: str) -> str:
    """Return localized welcome message for the user's locale."""
    welcome_text = "Welcome to our platform! We're excited to have you."
    return translate_welcome_message(welcome_text, user_locale)