from google.cloud import translate_v2 as translate
from storage_models import TranslationResult

def translate_text_google(text: str, target_language: str) -> TranslationResult:
    """
    Translates text using the Google Cloud Translation API.

    Args:
        text (str): The text to translate.
        target_language (str): The ISO 639-1 code for the target language (e.g., 'es', 'fr').

    Returns:
        A TranslationResult object.
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return TranslationResult(
        original_text=text,
        translated_text=result["translatedText"],
        target_language=target_language
    )
