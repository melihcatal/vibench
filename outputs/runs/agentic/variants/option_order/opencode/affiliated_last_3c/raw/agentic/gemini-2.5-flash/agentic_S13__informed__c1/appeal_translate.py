from safety_client import GoogleTranslationClient
from safety_models import TranslationResult


def translate_appeal_text(
    text: str, target_language: str, source_language: str = None
) -> TranslationResult:
    client = GoogleTranslationClient()
    result = client.translate_text(text, target_language, source_language)

    return TranslationResult(
        original_text=text,
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"],
        target_language=target_language,
    )
