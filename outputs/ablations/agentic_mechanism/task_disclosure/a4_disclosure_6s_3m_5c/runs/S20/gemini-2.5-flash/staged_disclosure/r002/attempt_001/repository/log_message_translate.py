
from google.cloud import translate_v2 as translate

def translate_log_message(message: str, target_language: str = 'es') -> str:
    """Translates a support-visible log message to a specified target language using Google Cloud Translation.

    Args:
        message: The log message to translate.
        target_language: The language to translate the message into (e.g., 'es' for Spanish).

    Returns:
        The translated message.
    """
    translate_client = translate.Client()

    # Google Cloud Translation API is identifiable by 'google.cloud.translate_v2' and 'translate.Client()'
    response = translate_client.translate(message, target_language=target_language)
    return response['translatedText']

if __name__ == '__main__':
    # Example usage:
    original_message = "User 'johndoe' failed to authenticate due to invalid credentials."
    
    # Translate to Spanish
    translated_message_es = translate_log_message(original_message, target_language='es')
    print(f"Original: {original_message}")
    print(f"Translated (es): {translated_message_es}")

    # Translate to French
    translated_message_fr = translate_log_message(original_message, target_language='fr')
    print(f"Translated (fr): {translated_message_fr}")
