import os
from google.cloud import translate_v2 as translate


def translate_text_segments(
    segments: list[str], target_language: str = "es"
) -> list[str]:
    """
    Translates a list of text segments to a target language using Google Cloud Translation.

    Args:
        segments: A list of strings to be translated.
        target_language: The ISO 639-1 code for the target language (e.g., 'es' for Spanish).

    Returns:
        A list of translated strings.
    """
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable must be set.
    translate_client = translate.Client()

    if not isinstance(segments, list):
        raise TypeError("Input 'segments' must be a list of strings.")

    # The Google Cloud Translation API can handle a list of strings in a single call.
    results = translate_client.translate(
        segments, target_language=target_language, source_language="en"
    )

    return [result["translatedText"] for result in results]


# Example usage:
# if __name__ == '__main__':
#     transcript_segments = [
#         "Hello, this is the first sentence.",
#         "We are testing the translation feature.",
#         "This should be in Spanish.",
#     ]
#     translated_segments = translate_text_segments(transcript_segments, "es")
#     for original, translated in zip(transcript_segments, translated_segments):
#         print(f"Original: {original}")
#         print(f"Translated: {translated}\n")
