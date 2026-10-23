import boto3


def invoice_note_translate(payload, config=None):
    client = boto3.client("translate", region_name=(config or {}).get("region"))
    text = payload.get("text", "")
    target_language = payload.get("target_language", "en")
    response = client.translate_text(Text=text, SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=target_language)
    return {"translated_text": response.get("TranslatedText", "")}
