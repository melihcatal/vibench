from translation_client import get_aws_translate_client, load_translation_config, normalize_language_code
from translation_models import TranslationResponse, normalize_text


def batch_translate(texts: list[str], source_language: str | None = None, target_language: str | None = None) -> list[TranslationResponse]:
    config = load_translation_config()
    client = get_aws_translate_client()
    target = normalize_language_code(target_language) or config.default_target_language
    source = normalize_language_code(source_language or config.default_source_language)
    responses: list[TranslationResponse] = []
    for text in texts:
        kwargs = {"Text": normalize_text(text), "TargetLanguageCode": target}
        if source:
            kwargs["SourceLanguageCode"] = source
        result = client.translate_text(**kwargs)
        responses.append(
            TranslationResponse(
                translated_text=result["TranslatedText"],
                source_language=result.get("SourceLanguageCode", source),
                target_language=result.get("TargetLanguageCode", target),
            )
        )
    return responses
