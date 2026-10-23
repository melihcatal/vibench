
from google.cloud import translate_v2 as translate
import os

def translate_text(text: str, target_language: str = "en") -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The language to translate to (e.g., "en", "es", "fr").

    Returns:
        The translated text.
    """
    # Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    # or credentials passed explicitly.
    # For more information, see:
    # https://cloud.google.com/docs/authentication/production
    
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    message = "Hello, how are you?"
    translated_message = translate_text(message, "es")
    print(f"Original: {message}")
    print(f"Translated (Spanish): {translated_message}")

    message_fr = "How do you do?"
    translated_message_fr = translate_text(message_fr, "fr")
    print(f"Original: {message_fr}")
    print(f"Translated (French): {translated_message_fr}")
