
from google.cloud import translate_v2 as translate

def translate_payload(text: str, target_language: str = 'en') -> str:
    """Translates text using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate to (e.g., 'en' for English, 'es' for Spanish).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    # Google Cloud Translation API can translate a string or a list of strings.
    # If you want to translate a list, pass an array of strings instead of a single string.
    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']

if __name__ == '__main__':
    # Example usage:
    # Set up your Google Cloud credentials (e.g., GOOGLE_APPLICATION_CREDENTIALS environment variable)
    # For more details, refer to: https://cloud.google.com/docs/authentication/getting-started
    
    message = "Hola, ¿cómo estás?"
    translated_message = translate_payload(message, target_language='en')
    print(f"Original: {message}")
    print(f"Translated: {translated_message}")

    message_es = "Hello, how are you?"
    translated_message_es = translate_payload(message_es, target_language='es')
    print(f"Original: {message_es}")
    print(f"Translated: {translated_message_es}")
