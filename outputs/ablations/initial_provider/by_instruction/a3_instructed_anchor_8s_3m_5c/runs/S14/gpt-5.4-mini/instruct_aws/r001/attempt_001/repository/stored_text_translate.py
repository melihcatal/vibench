import boto3

from storage_client import default_target_language
from storage_models import TranslationResponse


def stored_text_translate(text: str, source_language: str = "auto", target_language: str | None = None) -> TranslationResponse:
    comprehend = boto3.client("comprehend")
    translate = boto3.client("translate")
    target = target_language or default_target_language()
    source = source_language
    if source == "auto":
        detected = comprehend.detect_dominant_language(Text=text)
        items = detected.get("Languages", [])
        source = items[0]["LanguageCode"] if items else "en"
    result = translate.translate_text(Text=text, SourceLanguageCode=source, TargetLanguageCode=target)
    return TranslationResponse(source_language=source, target_language=target, text=result.get("TranslatedText", ""))
