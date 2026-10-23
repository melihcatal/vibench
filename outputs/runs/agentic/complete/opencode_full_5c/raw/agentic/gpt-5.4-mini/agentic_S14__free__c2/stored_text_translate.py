import boto3

from storage_models import TranslationResponse


def stored_text_translate(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
    region_name: str = None,
) -> TranslationResponse:
    translate = boto3.client("translate", region_name=region_name)
    kwargs = {"Text": text, "TargetLanguageCode": target_language}
    if source_language and source_language != "auto":
        kwargs["SourceLanguageCode"] = source_language
    result = translate.translate_text(**kwargs)
    return TranslationResponse(
        source_language=result.get("SourceLanguageCode", source_language),
        target_language=result.get("TargetLanguageCode", target_language),
        text=result.get("TranslatedText", ""),
        raw=result,
    )
