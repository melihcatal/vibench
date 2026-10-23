from google.cloud import translate_v2 as translate
from identity_models import OnboardingTranslationPayload
import os


def welcome_translate(payload: OnboardingTranslationPayload) -> dict:
    # Google Cloud Translation API requires GOOGLE_APPLICATION_CREDENTIALS to be set
    # or explicit client initialization with credentials.
    # For simplicity, assuming GOOGLE_APPLICATION_CREDENTIALS env var is set.
    
    translate_client = translate.Client()

    target_language = payload.target_language
    text_to_translate = payload.text

    # The target language must be a valid BCP-47 language code.
    result = translate_client.translate(text_to_translate, target_language=target_language)

    return {
        "original_text": text_to_translate,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language
    }
