import boto3


def invoice_note_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    text = payload.get("text") or payload.get("note") or ""
    response = client.translate_text(Text=text[:5000], SourceLanguageCode=config.get("source_language", "auto"), TargetLanguageCode=config.get("target_language", "en"))
    return {"translated_text": response.get("TranslatedText", "")}
