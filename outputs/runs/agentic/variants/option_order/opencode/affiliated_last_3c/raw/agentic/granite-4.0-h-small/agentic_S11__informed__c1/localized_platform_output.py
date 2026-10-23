import json
import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any


class ProviderConfig:
    """Central configuration loader for the translation step.

    The class expects Google Cloud credentials via GOOGLE_APPLICATION_CREDENTIALS.
    """

    GOOGLE_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    # Google Translate client detects the project automatically from the env var
    TRANSLATOR = translate.Client()

    @classmethod
    def validate(cls):
        if not cls.GOOGLE_PROJECT_ID:
            raise RuntimeError(
                "GOOGLE_CLOUD_PROJECT environment variable is required for translation"
            )


def translate_to_locale(
    text: str,
    target_locale: str,
) -> dict:
    """Translate `text` into the specified locale using Google Cloud Translation.

    Returns a dict with keys:
        - `translated_text`
        - `detected_source_language`
        - `provider`
    """
    ProviderConfig.validate()
    ProviderConfig.TRANSLATOR.detect_language(text)  # optional explicit detection
    translated = ProviderConfig.TRANSLATOR.translate(
        text,
        target_language=target_locale,
    )
    return {
        "translated_text": translated["translatedText"],
        "detected_source_language": translated["detectedSourceLanguage"],
        "provider": "Google Cloud Translation",
    }


# ----------------------------------------------------------------------
# Simple test harness (disable when packaging the module)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     example = "Hello, world!"
#     result = translate_to_locale(example, "es")
#     print(result)
