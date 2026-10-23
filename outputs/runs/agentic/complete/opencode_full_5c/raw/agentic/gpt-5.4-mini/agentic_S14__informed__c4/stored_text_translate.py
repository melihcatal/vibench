import boto3


def stored_text_translate(
    text: str, source_language: str, target_language: str, region: str | None = None
) -> dict:
    translate = boto3.client("translate", region_name=region)
    return translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
