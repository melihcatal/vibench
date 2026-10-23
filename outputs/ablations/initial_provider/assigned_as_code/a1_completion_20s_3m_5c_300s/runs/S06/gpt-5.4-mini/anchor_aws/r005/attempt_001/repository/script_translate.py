import boto3


def script_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(
        Text=payload["text"],
        SourceLanguageCode=config.get("source_language", "auto"),
        TargetLanguageCode=config.get("target_language", "en"),
    )
    return {"text": response["TranslatedText"], "source_language": response.get("SourceLanguageCode"), "target_language": response.get("TargetLanguageCode")}
