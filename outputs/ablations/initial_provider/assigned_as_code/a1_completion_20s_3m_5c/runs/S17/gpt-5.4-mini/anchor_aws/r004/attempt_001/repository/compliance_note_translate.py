import boto3


def compliance_note_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(
        Text=payload.get("text", ""),
        SourceLanguageCode=payload.get("source_language", "en"),
        TargetLanguageCode=payload.get("target_language", "en"),
    )
    return {"translated_text": response.get("TranslatedText")}
