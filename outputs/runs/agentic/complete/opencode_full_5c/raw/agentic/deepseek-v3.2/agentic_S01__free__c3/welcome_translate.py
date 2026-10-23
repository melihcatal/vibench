import os
from google.cloud import translate_v2 as translate
from identity_models import UserProfile


def translate_welcome_text(text: str, target_language: str = "en") -> str:
    """Translate onboarding text using Google Cloud Translation API."""
    # Initialize Google Cloud Translation client
    client = translate.Client()

    # Translate the text
    result = client.translate(text, target_language=target_language, format_="text")

    return result["translatedText"]


def get_user_welcome_message(user_profile: UserProfile) -> str:
    """Generate and translate welcome message for user based on their locale."""
    base_welcome = "Welcome to our platform! We're excited to have you join us. Please complete your profile to get started."

    # Determine target language from user profile
    target_language = user_profile.locale or "en"

    # Translate welcome message
    translated_welcome = translate_welcome_text(base_welcome, target_language)

    # Add personalized touch
    personalized_message = f"{translated_welcome}"
    if user_profile.name:
        personalized_message = f"Hello {user_profile.name}! {translated_welcome}"

    return personalized_message


def translate_onboarding_copy(copy_dict: dict, target_language: str) -> dict:
    """Translate multiple onboarding copy strings."""
    client = translate.Client()
    translated = {}

    for key, text in copy_dict.items():
        if text:
            result = client.translate(text, target_language=target_language)
            translated[key] = result["translatedText"]
        else:
            translated[key] = ""

    return translated
