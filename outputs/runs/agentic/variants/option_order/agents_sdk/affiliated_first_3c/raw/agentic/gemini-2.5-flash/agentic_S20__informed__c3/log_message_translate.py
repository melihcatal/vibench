import os
from observability_client import observability_client

def translate_log_message(text: str, target_language: str = "es") -> str:
    """
    Translates support-visible log messages for another locale using Google Cloud Translation.

    Args:
        text: The log message text to translate.
        target_language: The ISO 639-1 code of the target language (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = observability_client.get_translate_client()

    try:
        result = client.translate(text, target_language=target_language)
        translated_text = result["translatedText"]
        print(f"Original: '{text}' -> Translated ({target_language}): '{translated_text}'")
        return translated_text
    except Exception as e:
        print(f"Error translating text '{text}': {e}")
        return f"[Translation Error: {e}]"

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    messages_to_translate = [
        "Failed to connect to database.",
        "User 'admin' successfully logged in.",
        "Disk space critical on server 'web-01'."
    ]

    print("Translating log messages to Spanish (es)...")
    for msg in messages_to_translate:
        translate_log_message(msg, "es")

    print("\nTranslating log messages to French (fr)...")
    for msg in messages_to_translate:
        translate_log_message(msg, "fr")
