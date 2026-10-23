from google.cloud import translate_v2 as translate
from identity_models import UserProfile
import os

# Initialize Google Cloud Translation client
translate_client = translate.Client.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)


def welcome_translate(profile: UserProfile, text: str) -> str:
    if not profile.locale:
        return text

    result = translate_client.translate(
        text, target_language=profile.locale, format_="text"
    )
    return result["translatedText"]
