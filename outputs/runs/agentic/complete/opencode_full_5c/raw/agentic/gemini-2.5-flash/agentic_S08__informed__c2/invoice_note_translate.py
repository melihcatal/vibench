from document_models import TranslationResult
from document_client import get_translate_client


def translate_invoice_notes(
    text: str, target_language: str = "en"
) -> TranslationResult:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    """
    client = get_translate_client()

    translation = client.translate(text, target_language=target_language)

    return TranslationResult(
        translated_text=translation["translatedText"],
        source_language=translation["detectedSourceLanguage"],
        target_language=target_language,
    )
