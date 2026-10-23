import os
from google.cloud import translate_v2 as translate


def translate_onboarding_copy(text: str, target_language: str) -> str:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation.
    """
    # Google Cloud Translation client implicitly uses GOOGLE_APPLICATION_CREDENTIALS
    # or other default credentials if set up.
    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        raise RuntimeError(f"Google Cloud Translation failed: {e}")


if __name__ == "__main__":
    # Example usage (ensure GOOGLE_APPLICATION_CREDENTIALS is set up)
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    onboarding_text = "Welcome to our platform! Please complete your profile."
    target_locale = "es"  # Spanish

    try:
        translated_text = translate_onboarding_copy(onboarding_text, target_locale)
        print(f"Original: {onboarding_text}")
        print(f"Translated ({target_locale}): {translated_text}")
    except RuntimeError as e:
        print(f"Error: {e}")
