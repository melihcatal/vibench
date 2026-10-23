from google.cloud import translate_v2 as translate
from typing import Optional

def translate_log_message(
    text: str,
    target_language: str,
    source_language: Optional[str] = "en"
) -> Optional[dict]:
    """
    Translates a log message to another language using Google Cloud Translate API.

    This is useful for preparing logs for international support teams who may
    not be native English speakers.

    Args:
        text: The log message to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'es', 'fr', 'ja').
        source_language: The ISO 639-1 code for the source language (e.g., 'en').

    Returns:
        A dictionary containing the translated text and detected source language,
        or None if an error occurs.
    """
    try:
        # Instantiates a client. This will use Application Default Credentials.
        translate_client = translate.Client()

        # The text to translate.
        if isinstance(text, bytes):
            text = text.decode("utf-8")

        # Translates the text into the target language.
        result = translate_client.translate(
            text, 
            target_language=target_language,
            source_language=source_language
        )

        return result
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None

# Example usage:
# support_message = "User 'jdoe' failed to update profile due to invalid email format."
# translation_result = translate_log_message(support_message, target_language="es")
# if translation_result:
#     print(f"Original ('{translation_result['detectedSourceLanguage']}'): {support_message}")
#     print(f"Translated ('es'): {translation_result['translatedText']}")
