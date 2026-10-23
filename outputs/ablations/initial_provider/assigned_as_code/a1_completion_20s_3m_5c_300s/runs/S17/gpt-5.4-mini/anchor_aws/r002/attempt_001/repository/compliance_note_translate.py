import boto3


def compliance_note_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    text = payload.get("note") or payload.get("text") or ""
    response = client.translate_text(Text=text, SourceLanguageCode=config.get("source_language", "en"), TargetLanguageCode=config.get("target_language", "es"))
    return {"translated_text": response.get("TranslatedText")}
