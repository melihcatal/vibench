import boto3


def compliance_note_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(
        Text=payload["text"],
        SourceLanguageCode=config.get("source_language", "en"),
        TargetLanguageCode=config.get("target_language", "es"),
    )
    return {"translated_text": response["TranslatedText"]}
