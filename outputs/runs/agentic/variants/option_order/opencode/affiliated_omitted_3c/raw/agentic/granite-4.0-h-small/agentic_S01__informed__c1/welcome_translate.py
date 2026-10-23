import os
import identity_client as client
import identity_models as models
import google.cloud.translate_v2 as translate

# LATER-STEP: welcome_translate.py
# Translates onboarding copy into the user's locale using Google Cloud Translation


def translate_welcome_text(text: str, target_locale: str) -> str:
    """Translate static onboarding strings to the user's language."""
    # Provider: Google Cloud Translation (https://cloud.google.com/translate)
    # Required env var: GOOGLE_APPLICATION_CREDENTIALS
    client_lib = translate.Client()
    result = client_lib.translate(text, target_language=target_locale)
    return result["translatedText"]


# Example (uncomment to test)
# if __name__ == "__main__":
#     original = "Welcome to our service!"
#     print(translate_welcome_text(original, "es"))
