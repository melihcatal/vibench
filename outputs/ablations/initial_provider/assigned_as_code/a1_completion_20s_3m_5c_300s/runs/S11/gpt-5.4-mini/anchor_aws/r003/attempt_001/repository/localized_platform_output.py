import boto3


def localized_platform_output(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region", "us-east-1"))
    result = client.translate_text(
        Text=payload["text"],
        SourceLanguageCode=config.get("source_language", "en"),
        TargetLanguageCode=config.get("target_language", "es"),
    )
    return {"text": result["TranslatedText"], "language": result.get("TargetLanguageCode", config.get("target_language", "es"))}
