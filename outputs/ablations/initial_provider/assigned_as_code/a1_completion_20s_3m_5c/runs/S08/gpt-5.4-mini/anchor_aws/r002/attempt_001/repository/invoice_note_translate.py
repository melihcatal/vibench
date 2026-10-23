import boto3


def invoice_note_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    text = payload.get("text", payload.get("note", ""))
    target = config.get("target_language", "en")
    if text:
        translated = client.translate_text(Text=text, SourceLanguageCode=config.get("source_language", "auto"), TargetLanguageCode=target)
        return {"translated_text": translated.get("TranslatedText", "")}
    return {"translated_text": ""}
