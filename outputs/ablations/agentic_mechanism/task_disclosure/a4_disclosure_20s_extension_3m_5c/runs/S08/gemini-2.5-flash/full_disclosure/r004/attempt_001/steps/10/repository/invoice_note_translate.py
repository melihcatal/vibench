
from google.cloud import translate_v2 as translate

def translate_invoice_note(text: str, target_language: str = 'en') -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.

    Args:
        text: The text to be translated.
        target_language: The target language for the translation (default is English 'en').

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']
