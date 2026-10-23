import boto3


def payload_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    text = payload.get("text") or payload.get("message") or ""
    result = client.translate_text(Text=text, SourceLanguageCode=config.get("source_language", "auto"), TargetLanguageCode=config.get("target_language", "en"))
    return {"translated_text": result.get("TranslatedText"), "source_language": result.get("SourceLanguageCode"), "target_language": result.get("TargetLanguageCode")}
