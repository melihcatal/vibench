import os
from google.cloud import translate_v2 as translate

def translate_html(text, target_language, source_language=None):
    """Translates HTML text using Google Cloud Translation while preserving tags."""
    client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(
        text, target_language=target_language, format_='html', source_language=source_language
    )

    return result["translatedText"]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Translate HTML/markup while preserving tags.")
    parser.add_argument("text", help="The HTML or markup text to translate.")
    parser.add_argument("target_language", help="The target language for translation (e.g., 'es', 'fr').")
    parser.add_argument("--source_language", help="Optional: The source language (e.g., 'en'). If not provided, it will be auto-detected.")

    args = parser.parse_args()

    # This check is for user awareness and to guide them on setup.
    # In a real environment, GOOGLE_APPLICATION_CREDENTIALS should be set or
    # other authentication methods (like GKE workload identity) should be used.
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
        print("Please set it to the path of your Google Cloud service account key file.")
        print("For more information, refer to Google Cloud Translation API documentation.")
        # Exit or handle error gracefully if credentials are critical for immediate execution
        # For this example, we'll proceed, assuming it might be handled externally or for testing without actual API calls.

    translated_text = translate_html(args.text, args.target_language, args.source_language)
    print(translated_text)