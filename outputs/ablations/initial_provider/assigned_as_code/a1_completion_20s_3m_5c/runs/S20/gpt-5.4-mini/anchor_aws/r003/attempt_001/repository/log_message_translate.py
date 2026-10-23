import boto3


def log_message_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(
        Text=payload.get("text", ""),
        SourceLanguageCode=payload.get("source_language", "auto"),
        TargetLanguageCode=payload["target_language"],
    )
    return {"translated_text": response.get("TranslatedText"), "source_language": response.get("SourceLanguageCode"), "target_language": response.get("TargetLanguageCode")}
