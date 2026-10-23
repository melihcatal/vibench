from safety_client import get_google_translate_client
from safety_models import TranslationResult


def translate_appeal(text: str, target_language: str = "en") -> TranslationResult:
    client = get_google_translate_client()

    result = client.translate(text, target_language=target_language)

    return TranslationResult(
        original_text=text,
        translated_text=result["translatedText"],
        target_language=target_language,
    )
