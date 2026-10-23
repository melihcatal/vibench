import boto3
from storage_client import download_text


def translate_stored_text(
    key: str, source_language: str = "en", target_language: str = "es"
) -> str:
    text = download_text(key)
    translate_client = boto3.client("translate")
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return result["TranslatedText"]
