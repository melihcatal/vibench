
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = 'en') -> str:
    """Translates text into the target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate to (e.g., 'en' for English, 'es' for Spanish).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    # Google Cloud Translation API is the concrete external provider
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    # Example usage:
    message = "Hola, ¿cómo estás?"
    translated_message = translate_text(message, target_language='en')
    print(f"Original: {message}")
    print(f"Translated (English): {translated_message}")

    message = "Hello, how are you?"
    translated_message = translate_text(message, target_language='es')
    print(f"Original: {message}")
    print(f"Translated (Spanish): {translated_message}")
