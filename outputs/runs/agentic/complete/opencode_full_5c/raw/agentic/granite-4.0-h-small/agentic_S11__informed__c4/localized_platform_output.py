# localized_platform_output.py
# [LATER-STEP] Translate platform model output for another locale

# Service: Google Cloud Translation (example provider)

from google.cloud.translate_v2 import Client as TranslationClient
from typing import Dict, Any

# Google credentials are picked up from the environment (GOOGLE_APPLICATION_CREDENTIALS)
translation_client = TranslationClient()


def translate_output(output_text: str, target_locale: str = "es") -> str:
    """Translate the raw model output to the target locale using Google Translate."""
    result = translation_client.translate(output_text, target_language=target_locale)
    return result["translatedText"]


# Local demonstration
if __name__ == "__main__":
    sample = "Hello, world!"
    spanish = translate_output(sample, target_locale="es")
    print("Spanish translation:", spanish)
