from google.cloud import translate_v2 as translate

def translate_payload(text: str, target_language: str = "es") -> str:
    """Translates text using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate to (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    message = "Hello, how are you?"
    translated_message = translate_payload(message, "fr")
    print(f"Original: {message}")
    print(f"Translated (French): {translated_message}")

    message_spanish = translate_payload("This is a customer-facing message.", "es")
    print(f"Original: This is a customer-facing message.")
    print(f"Translated (Spanish): {message_spanish}")
