
from google.cloud import translate_v2 as translate

def translate_payload_text(text: str, target_language: str) -> str:
    """Translates text using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    message = "Hello, how are you doing today? We hope you enjoy our service."
    translated_message = translate_payload_text(message, "es")
    print(f"Original: {message}")
    print(f"Translated (Spanish): {translated_message}")

    message_french = "This is a test message for translation."
    translated_message_french = translate_payload_text(message_french, "fr")
    print(f"Original: {message_french}")
    print(f"Translated (French): {translated_message_french}")
