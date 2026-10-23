import os
import json
from typing import Any

# Use the Google Cloud Translation SDK as the concrete provider.
# Set env var GOOGLE_APPLICATION_CREDENTIALS to point to a service account JSON.
from google.cloud import translate_v2 as translate

TRANSLATOR = translate.Client()


def translate_script(script_path: str, target_lang: str = "es") -> str:
    """
    Translate a narration script (plain text file) from its current language
    to the target language using Google Cloud Translation.
    Returns the translated script as a string.
    """
    with open(script_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    # Detect language if needed
    result = TRANSLATOR.detect_language(original_text)
    print(f"Detected language: {result['language']}, confidence: {result['confidence']}")

    translated = TRANSLATOR.translate(original_text, target_language=target_lang)
    return translated['translatedText']


def translate_and_save(script_path: str, output_path: str, target_lang: str = "es"):
    """Translate and write the result to a file."""
    translated = translate_script(script_path, target_lang)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(translated)
    return output_path

# Example CLI usage (remove when used as a library)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Translate narration script before TTS")
    parser.add_argument("script", help="Path to input script file")
    parser.add_argument("output", help="Path for translated script")
    parser.add_argument("--lang", default="es", help="Target language code, e.g., es, fr")
    args = parser.parse_args()
    print(translate_and_save(args.script, args.output, args.lang))
