from google.cloud import translate_v2 as translate

def translate_log_message(text: str, target_language: str) -> str:
    """Translates a log message to a specified target language using Google Cloud Translation API.

    Args:
        text: The log message text to translate.
        target_language: The language code to translate the message into (e.g., "es" for Spanish).

    Returns:
        The translated log message.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    message = "User login failed due to invalid credentials."
    translated_message = translate_log_message(message, "es")
    print(f"Original: {message}")
    print(f"Translated (es): {translated_message}")
