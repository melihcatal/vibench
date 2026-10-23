import os
from google.cloud import translate_v2 as translate
from identity_models import ConsentTranslation

# Using Google Cloud Translation API
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project")


def translate_consent(provider_text: str, target_locale: str) -> ConsentTranslation:
    """Translates identity-provider consent copy using Google Cloud Translation API."""
    translate_client = translate.Client()

    result = translate_client.translate(provider_text, target_language=target_locale)

    return ConsentTranslation(
        provider_text=provider_text,
        translated_text=result["translatedText"],
        locale=target_locale,
    )
