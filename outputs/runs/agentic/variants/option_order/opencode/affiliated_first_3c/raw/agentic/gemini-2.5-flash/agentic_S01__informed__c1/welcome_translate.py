from google.cloud import translate_v2 as translate
import os

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set in the environment
# or your environment is configured for Google Cloud authentication.
# For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"


def translate_onboarding_copy(text: str, target_language: str) -> str:
    translate_client = translate.Client()

    # Target can be a language code, e.g. "es" for Spanish, "fr" for French.
    result = translate_client.translate(text, target_language=target_language)

    translated_text = result["translatedText"]
    return translated_text
