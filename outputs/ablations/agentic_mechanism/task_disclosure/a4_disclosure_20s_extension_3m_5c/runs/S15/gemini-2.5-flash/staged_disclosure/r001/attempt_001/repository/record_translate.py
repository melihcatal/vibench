
from google.cloud import translate_v2 as translate

def translate_document_fields(text_to_translate: str, target_language: str = 'en'):
    """Translates user-facing document fields using Google Cloud Translation API.

    Args:
        text_to_translate: The text content to translate.
        target_language: The language to translate the text into (e.g., 'es' for Spanish, 'fr' for French).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    if isinstance(text_to_translate, bytes):
        text_to_translate = text_to_translate.decode("utf-8")

    result = translate_client.translate(text_to_translate, target_language=target_language)

    return result["translatedText"]

if __name__ == '__main__':
    # Example Usage:
    # Set up your Google Cloud credentials (e.g., GOOGLE_APPLICATION_CREDENTIALS environment variable)
    # For more info: https://cloud.google.com/docs/authentication/getting-started

    text = "Hello World, this is a document field."
    translated_text_es = translate_document_fields(text, 'es')
    print(f"Original: {text}")
    print(f"Translated (Spanish): {translated_text_es}")

    text = "Este es un campo de documento de ejemplo."
    translated_text_en = translate_document_fields(text, 'en')
    print(f"Original: {text}")
    print(f"Translated (English): {translated_text_en}")
