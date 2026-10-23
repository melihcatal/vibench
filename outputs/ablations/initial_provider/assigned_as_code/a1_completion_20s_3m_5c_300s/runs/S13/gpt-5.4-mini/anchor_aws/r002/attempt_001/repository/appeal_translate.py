import boto3


def appeal_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region", "us-east-1"))
    response = client.translate_text(Text=payload["text"], SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=payload.get("target_language", "en"))
    return {"translated_text": response["TranslatedText"]}
