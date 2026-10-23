
from google.cloud import translate_v2 as translate

def translate_log_message(message: str, target_language: str = "es") -> str:
    """Translates a log message to a specified target language using Google Cloud Translation.

    Args:
        message: The log message to translate.
        target_language: The language to translate the message into (e.g., "es" for Spanish).

    Returns:
        The translated message.
    """
    translate_client = translate.Client()
    result = translate_client.translate(message, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    original_message = "User 'johndoe' failed to authenticate due to invalid password."
    translated_message = translate_log_message(original_message, target_language="es")
    print(f"Original: {original_message}")
    print(f"Translated (es): {translated_message}")

    original_message_2 = "Error: Database connection lost."
    translated_message_2 = translate_log_message(original_message_2, target_language="fr")
    print(f"Original: {original_message_2}")
    print(f"Translated (fr): {translated_message_2}")
