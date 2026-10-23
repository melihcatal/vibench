import os
from google.cloud import translate_v2 as translate
from identity_client import config
from identity_models import TranslationResult


def translate_consent_copy(
    text: str, target_language: str, source_language: str = "en"
) -> TranslationResult:
    # GOOGLE_APPLICATION_CREDENTIALS identifies the Google Cloud Translation service
    # The 'google-cloud-translate' SDK also makes it identifiable.

    # Ensure GOOGLE_APPLICATION_CREDENTIALS env var is set or authenticated in another way
    # For local development, `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"`

    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
    )

    return TranslationResult(
        original_text=text,
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"],
        target_language=target_language,
    )
