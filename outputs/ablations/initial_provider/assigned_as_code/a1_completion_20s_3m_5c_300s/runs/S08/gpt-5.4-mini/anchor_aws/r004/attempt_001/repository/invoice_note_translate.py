import boto3


def invoice_note_translate(payload, config=None):
    client = boto3.client("translate", region_name=(config or {}).get("region"))
    text = payload.get("text", "")
    response = client.translate_text(Text=text, SourceLanguageCode=(config or {}).get("source_language", "auto"), TargetLanguageCode=(config or {}).get("target_language", "en"))
    return {"translated_text": response.get("TranslatedText", ""), "source_language": response.get("SourceLanguageCode"), "target_language": response.get("TargetLanguageCode")}
