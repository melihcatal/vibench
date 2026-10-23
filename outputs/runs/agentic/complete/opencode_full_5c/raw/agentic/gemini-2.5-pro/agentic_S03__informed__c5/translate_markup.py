from translation_client import get_translation_client
from translation_models import TranslationResponse


def translate_markup(
    markup: str, source_language: str, target_language: str
) -> TranslationResponse:
    """
    Translates HTML content using Google Cloud Translation, preserving markup.
    """
    client = get_translation_client()

    result = client.translate(
        markup,
        target_language=target_language,
        source_language=source_language,
        format_="html",
    )

    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage"),
    )
