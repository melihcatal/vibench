import boto3


def vendor_text_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("text") or payload.get("vendor_notes") or ""
    response = client.detect_pii_entities(Text=text[:1000], LanguageCode=config.get("language_code", "en"))
    return {"safe": not response.get("Entities"), "entities": response.get("Entities", [])}
