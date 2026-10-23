import json
import os
from google.cloud import translate_v2 as translate

def translate_description(description: str, target_language: str = "en") -> str:
    """Translate a generated image description to another language using Google Cloud Translation API.",
    """Returns the translated description.",
    """
    client = translate.Client()
    # Translate the text
    result = client.translate(description, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Translate a description")
    parser.add_argument("description", type=str, help="Original description text")
    parser.add_argument("target", type=str, default="en", help="Target language code (default: en)")
    args = parser.parse_args()
    translated = translate_description(args.description, args.target)
    print(translated)
