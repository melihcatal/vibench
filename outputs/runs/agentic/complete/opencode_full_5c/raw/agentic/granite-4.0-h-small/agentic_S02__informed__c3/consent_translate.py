import os
from google.cloud.translate_v2 import Client

# Google Identity Platform OIDC reference
# service: Google Identity Platform
# interface: sdk_or_rest
# auth: GOOGLE_APPLICATION_CREDENTIALS

TRANSLATE_TARGET = os.getenv("TRANSLATE_TARGET_LANG", "es")


def translate_consent(consent_text: str) -> str:
    translate_client = Client()
    translated = translate_client.translate(
        consent_text, target_language=TRANSLATE_TARGET
    )
    return translated["translatedText"]


if __name__ == "__main__":
    sample = "Please agree to share your email address and profile picture."
    print(translate_consent(sample))
