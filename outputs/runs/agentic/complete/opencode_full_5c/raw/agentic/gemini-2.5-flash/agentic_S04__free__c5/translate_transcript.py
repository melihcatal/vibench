import os
import sys
from google.cloud import translate_v2 as translate
from typing import List


def translate_segments(
    text_segments: List[str], target_language: str = "es"
) -> List[str]:
    """
    Translates a list of text segments using Google Cloud Translation API.

    Args:
        text_segments: A list of strings, where each string is a transcript segment.
        target_language: The target language code (e.g., "es" for Spanish, "fr" for French).

    Returns:
        A list of translated strings.
    """
    client = translate.Client()

    translations = []
    for text in text_segments:
        # The actual translation happens here
        result = client.translate(text, target_language=target_language)
        translations.append(result["translatedText"])
        print(
            f"Translated '{text}' to '{result['translatedText']}' ({target_language})"
        )

    return translations


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python translate_transcript.py <text_segment1> [text_segment2 ...] [target_language]"
        )
        print('Example: python translate_transcript.py "Hello world" "How are you" es')
        sys.exit(1)

    # The last argument can be the target language if it's a valid language code (2-letter)
    # Otherwise, all arguments are treated as text segments.
    if len(sys.argv) > 1 and len(sys.argv[-1]) == 2 and sys.argv[-1].isalpha():
        target_language = sys.argv[-1].lower()
        text_segments = sys.argv[1:-1]
    else:
        target_language = "es"  # Default to Spanish
        text_segments = sys.argv[1:]

    if not text_segments:
        print("No text segments provided for translation.")
        sys.exit(1)

    # For demonstration, ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    try:
        translated_texts = translate_segments(text_segments, target_language)
        print("\n--- Translated Results ---")
        for original, translated in zip(text_segments, translated_texts):
            print(f"Original: {original}")
            print(f"Translated: {translated}\n")
    except Exception as e:
        print(f"Error translating text: {e}")
        sys.exit(1)
