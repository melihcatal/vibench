# LATER-STEP: consent_translate.py
# Translate identity-provider consent copy (privacy policy / terms) for end‑user display

import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation configuration (uses env var)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize client
translate_client = translate.Client()


# Translation helper
def translate_consent(copy_text: str, target_lang: str = "es") -> str:
    """
    Translate consent text to the target language (default Spanish).
    Returns the translated string.
    """
    result = translate_client.translate(copy_text, target_language=target_lang)
    return result["translatedText"]


# Example pairing: provider --> language map (configurable)
CONSENT_TEXT = {
    "google": "We need access to your email address and profile to log you in.",
    "auth0": "We will store your ID token and profile information.",
    "openid": "Our service requires consent for OpenID Connect scopes.",
}


# Example usage (CLI)
def main():
    provider = input("Enter provider name (google, auth0, openid): ").lower()
    if provider not in CONSENT_TEXT:
        print("Unsupported provider")
        return
    original = CONSENT_TEXT[provider]
    translated = translate_consent(original)
    print("\nOriginal consent copy:")
    print(original)
    print("\nTranslated copy (es):")
    print(translated)


if __name__ == "__main__":
    main()
