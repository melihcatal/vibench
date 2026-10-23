import os
from google.cloud import translate_v2 as translate
from identity_models import RegisterUserResponse

# Initialize Google Cloud Translation client
translate_client = translate.Client()


def translate_welcome_message(user_locale: str, text: str) -> str:
    if not user_locale or user_locale == "en":
        return text
    
    result = translate_client.translate(
        text,
        target_language=user_locale,
        model="nmt"  # Use Neural Machine Translation model
    )
    return result["translatedText"]


def get_localized_welcome(user: RegisterUserResponse, user_locale: str) -> str:
    welcome_text = f"Welcome, {user.user_id}! Your account has been created successfully."
    return translate_welcome_message(user_locale, welcome_text)