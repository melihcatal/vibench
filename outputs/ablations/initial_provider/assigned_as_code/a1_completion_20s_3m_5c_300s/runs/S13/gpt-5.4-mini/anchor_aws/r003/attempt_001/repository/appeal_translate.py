import boto3


def appeal_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region", "us-east-1"))
    text = payload.get("text", "") if isinstance(payload, dict) else str(payload)
    source = config.get("source_language_code", "auto")
    target = config.get("target_language_code", "en")
    response = client.translate_text(Text=text, SourceLanguageCode=source, TargetLanguageCode=target)
    return {"translated_text": response.get("TranslatedText", "")}
