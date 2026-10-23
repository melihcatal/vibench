import boto3


def vendor_text_safety(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text", "")
    response = client.detect_pii_entities(Text=text, LanguageCode="en")
    return {"redacted": text, "entities": response.get("Entities", [])}
