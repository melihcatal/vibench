from model_client import get_google_translate_client
from model_models import TranslationResponse


def translate_text(text: str, target_language: str) -> TranslationResponse:
    translate_client = get_google_translate_client()

    result = translate_client.translate(text, target_language=target_language)

    return TranslationResponse(
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"],
    )
