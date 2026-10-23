from storage_client import get_translate_client
from storage_models import TranslationResult


def translate_text(
    text: str, target_language: str, source_language: str = "auto"
) -> TranslationResult | None:
    translate_client = get_translate_client()
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        return TranslationResult(
            source_language=response["SourceLanguageCode"],
            translated_text=response["TranslatedText"],
        )
    except Exception as e:
        print(f"Error translating text: {e}")
        return None
