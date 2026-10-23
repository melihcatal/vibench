
from google.cloud import translate_v2 as translate

def translate_log_message(message: str, target_language: str = "es") -> str:
    """Translates a log message to a specified target language using Google Cloud Translation.

    Args:
        message: The log message to translate.
        target_language: The language to translate the message to (e.g., "es" for Spanish).

    Returns:
        The translated message.
    """
    translate_client = translate.Client()
    result = translate_client.translate(message, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    # Example usage
    log_message = "User 'johndoe' failed to authenticate due to invalid password."
    translated_message = translate_log_message(log_message, "es")
    print(f"Original message: {log_message}")
    print(f"Translated message (es): {translated_message}")

    log_message_ja = "File 'report.docx' not found in the specified directory."
    translated_message_ja = translate_log_message(log_message_ja, "ja")
    print(f"Original message: {log_message_ja}")
    print(f"Translated message (ja): {translated_message_ja}")
