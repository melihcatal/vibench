from translation_client import get_translation_client
from translation_models import TranslationResponse


def translate_text(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResponse:
    """
    Translates a single text string.
    """
    client = get_translation_client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language if source_language else "",
    )
    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage"),
    )
