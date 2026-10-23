import boto3


def payload_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(Text=payload["text"], SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=payload["target_language"])
    return {"translated_text": response["TranslatedText"]}
