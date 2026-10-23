import json
from google.cloud import translate_v2 as translate

# LATER-STEP: Translate onboarding welcome message into user's locale


def translate_welcome(user_locale: str, message_key: str) -> str:
    """Retrieve and translate the onboarding copy for a given locale.

    Args:
        user_locale: BCP-47 locale code (e.g., 'es-ES', 'fr').
        message_key: Identifier for the onboarding copy in the manifest (e.g., 'welcome.title').

    Returns:
        str: Translated text.
    """
    # Load a static manifest that maps keys to base English strings
    with open("onboarding_manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
    base_text = manifest.get(message_key)
    if not base_text:
        raise ValueError(f"Missing onboarding copy for key '{message_key}'")
    # Google Cloud Translation client automatically picks credentials from GOOGLE_APPLICATION_CREDENTIALS
    translate_client = translate.Client()
    result = translate_client.translate(base_text, target_language=user_locale)
    # The API returns text under the key 'translatedText'
    return result["translatedText"]


# Example onboarding_manifest.json (must exist in same directory)
# {
#   "welcome.title": "Welcome to ExampleApp!",
#   "welcome.subtitle": "Create your account and get started."
# }
