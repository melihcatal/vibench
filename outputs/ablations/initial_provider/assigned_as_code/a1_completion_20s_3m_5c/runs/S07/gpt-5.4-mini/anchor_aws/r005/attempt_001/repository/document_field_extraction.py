import boto3


def document_field_extraction(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_entities(Text=payload["text"], LanguageCode=payload.get("language", "en"))
    return {"fields": response.get("Entities", [])}
