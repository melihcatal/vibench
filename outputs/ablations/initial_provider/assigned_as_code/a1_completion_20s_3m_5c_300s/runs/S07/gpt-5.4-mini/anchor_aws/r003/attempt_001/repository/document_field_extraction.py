import boto3


def document_field_extraction(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("text", "")
    response = client.detect_entities(Text=text, LanguageCode=config.get("language", "en"))
    fields = [{"type": item.get("Type"), "text": item.get("Text"), "score": item.get("Score")} for item in response.get("Entities", [])]
    return {"fields": fields, "raw": response}
