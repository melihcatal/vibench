from translation_client import get_aws_translate_client, load_translation_config, normalize_language_code
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(text: str, source_language: str | None = None, target_language: str | None = None) -> TranslationResponse:
    config = load_translation_config()
    client = get_aws_translate_client()
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=normalize_language_code(source_language or config.default_source_language),
        target_language=normalize_language_code(target_language) or config.default_target_language,
    )
    kwargs = {
        "Text": request.text,
        "TargetLanguageCode": request.target_language,
    }
    if request.source_language:
        kwargs["SourceLanguageCode"] = request.source_language
    result = client.translate_text(**kwargs)
    return TranslationResponse(
        translated_text=result["TranslatedText"],
        source_language=result.get("SourceLanguageCode", request.source_language),
        target_language=result.get("TargetLanguageCode", request.target_language),
    )
