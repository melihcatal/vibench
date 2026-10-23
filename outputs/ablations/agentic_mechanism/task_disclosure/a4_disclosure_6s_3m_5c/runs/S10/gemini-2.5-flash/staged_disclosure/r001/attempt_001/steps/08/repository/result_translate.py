
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

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    # Example usage:
    text_to_translate = "Hola mundo"
    translated_text = translate_text(text_to_translate, target_language='en')
    print(f"Original text: {text_to_translate}")
    print(f"Translated text: {translated_text}")

    text_to_translate_french = "Hello world"
    translated_text_french = translate_text(text_to_translate_french, target_language='fr')
    print(f"Original text: {text_to_translate_french}")
    print(f"Translated text: {translated_text_french}")
