import os
from google.cloud import translate_v2 as translate


def translate_welcome_message(text: str, target_locale: str) -> str:
    """Translates onboarding copy into the user's locale using Google Cloud Translation."""
    # Google Cloud Translation API identifies itself via GOOGLE_APPLICATION_CREDENTIALS
    # or other standard GCP authentication mechanisms.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # running in a GCP environment with appropriate permissions.

    # Explicitly check for the credential environment variable for clarity
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS not set. Defaulting to application default credentials."
        )

    translate_client = translate.Client()
    try:
        result = translate_client.translate(text, target_language=target_locale)
        return result["translatedText"]
    except Exception as e:
        raise ValueError(
            f"Failed to translate text using Google Cloud Translation: {e}"
        )
