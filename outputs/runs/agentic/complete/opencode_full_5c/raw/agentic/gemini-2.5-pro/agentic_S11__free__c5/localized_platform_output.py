from model_client import get_google_translate_client
from model_models import TranslationResponse


def localized_platform_output(
    text: str, target_language: str = "fr"
) -> TranslationResponse:
    """
    Translate platform model output for another locale using Google Cloud Translate.
    """
    client = get_google_translate_client()

    result = client.translate(text, target_language=target_language)

    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result["detectedSourceLanguage"],
    )
