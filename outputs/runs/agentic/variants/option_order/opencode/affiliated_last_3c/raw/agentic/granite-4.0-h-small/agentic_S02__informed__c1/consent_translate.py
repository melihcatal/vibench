import os
import json
from typing import Dict, Any

# Translation using Google Cloud Translation (REST API) as an example

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS env var to path of JSON key")

from google.cloud import translate_v2 as translate

client = translate.Client()


def translate_consent(consent_text: str, target_lang: str = "es") -> str:
    """Translate identity-provider consent copy into the requested language.

    Uses Google Cloud Translation API's simple REST client (google-cloud-translate).
    The function returns the translated string.
    """
    if not consent_text:
        return ""
    result = client.translate(
        consent_text,
        target_language=target_lang,
        source_language="en",  # assume source is English
    )
    return result["translatedText"]


# Example CLI for quick testing
if __name__ == "__main__":
    demo = "I agree to share my email address and name with the service provider."
    print("Original:", demo)
    print("Translated to Spanish:", translate_consent(demo, target_lang="es"))
