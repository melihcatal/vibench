# localized_platform_output.py
# Later-step scored file: Translate platform model output for another locale (Google Cloud Translation)

import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any

# Provider configuration (Google Cloud)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/path/to/gcp-credentials.json")

# Initialize client once (singleton pattern recommended in production)
translator = translate.Client()


def translate_output(text: str, target_locale: str = "fr") -> Dict[str, Any]:
    """
    Translate the given text into the requested target locale using Google Cloud Translation API.

    Args:
        text (str): The model output to translate.
        target_locale (str): BCP-47 language code (e.g., 'es', 'de', 'fr').

    Returns:
        Dict[str, Any]: Normalized translation result containing original text, target, translated text, and additional metadata.
    """
    response = translator.translate(text, target_language=target_locale)
    return {
        "original": text,
        "target_locale": target_locale,
        "translated_text": response["translatedText"],
        "input_tokens": response.get("input", "")
    }

# Example usage (uncomment to test)
#if __name__ == "__main__":
#    sample = "The quick brown fox jumps over the lazy dog."
#    print(translate_output(sample, target_locale="es"))
