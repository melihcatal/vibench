import boto3


def ocr_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    source_text = payload.get("text", "")
    response = client.translate_text(
        Text=source_text,
        SourceLanguageCode=config.get("source_language", "auto"),
        TargetLanguageCode=config.get("target_language", "en"),
    )
    return {"translated_text": response.get("TranslatedText", ""), "raw": response}
