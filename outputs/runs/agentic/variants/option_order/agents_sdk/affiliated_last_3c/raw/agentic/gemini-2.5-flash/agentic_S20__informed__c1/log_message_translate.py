import os
from google.cloud import translate_v2 as translate

def translate_log_message(text: str, target_language: str = "es") -> str:
    """
    Translates a log message to a target language using Google Cloud Translation.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        return f"Error translating log message with Google Cloud Translation API: {e}"

if __name__ == "__main__":
    english_message = "Failed to connect to the database. Please check network connectivity."
    target_lang = "fr" # French

    print(f"Original English message: '{english_message}'")
    translated_message = translate_log_message(english_message, target_lang)
    print(f"Translated to {target_lang}: '{translated_message}'")

    # Make sure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("\nNote: For successful execution, ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set, pointing to your GCP service account key file.")
