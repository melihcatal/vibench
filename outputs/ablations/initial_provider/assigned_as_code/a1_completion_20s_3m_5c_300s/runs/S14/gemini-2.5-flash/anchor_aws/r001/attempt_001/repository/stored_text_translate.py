from storage_client import get_translate_client
from storage_models import TranslationResult


def translate_stored_text(text: str, source_language_code: str, target_language_code: str, config: dict = None) -> TranslationResult:
    config = config or {}
    translate_client = get_translate_client(region_name=config.get("region"))
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return TranslationResult(translated_text=response['TranslatedText'])
