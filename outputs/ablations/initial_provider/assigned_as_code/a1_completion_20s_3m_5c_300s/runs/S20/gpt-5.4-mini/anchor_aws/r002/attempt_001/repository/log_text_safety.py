import boto3


def log_text_safety(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text", "")
    response = client.detect_pii_entities(Text=text, LanguageCode=payload.get("language", "en"))
    unsafe = bool(response.get("Entities"))
    return {"unsafe": unsafe, "entities": response.get("Entities", [])}
