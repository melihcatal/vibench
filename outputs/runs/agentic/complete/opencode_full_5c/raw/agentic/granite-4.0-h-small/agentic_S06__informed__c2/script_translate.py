# [LATER-STEP] script_translate.py
# Translate narration scripts before synthesis using Google Cloud Translation

import os
from google.cloud import translate_v2 as translate

# Load credentials from environment variable
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError(
        "Set GOOGLE_APPLICATION_CREDENTIALS env var to point to a service account JSON file"
    )

# Initialize translation client (singleton for reuse)
translator = translate.Client()


def translate_script(script: str, target_lang: str = "es") -> str:
    """Translate the given narration script to the target language.

    Args:
        script (str): Original narration text.
        target_lang (str): ISO 639-1 language code, e.g., "fr", "ja".

    Returns:
        str: Translated script ready for TTS.
    """
    result = translator.translate(script, target_language=target_lang)
    return result["translatedText"]


# Example usage
if __name__ == "__main__":
    original = "Hello, welcome to the demo. Let's translate this to French."
    french = translate_script(original, target_lang="fr")
    print("French version:", french)
