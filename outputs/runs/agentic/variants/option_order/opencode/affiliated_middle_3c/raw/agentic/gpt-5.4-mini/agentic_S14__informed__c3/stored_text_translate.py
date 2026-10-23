import boto3


def translate_stored_text(
    text: str,
    source_language: str,
    target_language: str,
    region_name: str | None = None,
):
    client = boto3.client("translate", region_name=region_name)
    return client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
