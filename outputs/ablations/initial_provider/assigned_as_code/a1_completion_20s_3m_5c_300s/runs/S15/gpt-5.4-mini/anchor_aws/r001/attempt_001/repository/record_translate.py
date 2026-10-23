import boto3


def record_translate(payload, config=None):
    client = boto3.client("translate", region_name=(config or {}).get("region"))
    text = payload.get("text") or payload.get("document", {}).get("text") or ""
    response = client.translate_text(Text=text, SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=payload["target_language"])
    return {"translated_text": response.get("TranslatedText"), "source_language": response.get("SourceLanguageCode"), "target_language": response.get("TargetLanguageCode")}
