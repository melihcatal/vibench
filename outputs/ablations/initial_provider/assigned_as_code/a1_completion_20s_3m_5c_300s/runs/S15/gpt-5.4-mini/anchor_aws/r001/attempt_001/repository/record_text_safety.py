import boto3


def record_text_safety(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text") or payload.get("document", {}).get("text") or ""
    response = client.detect_pii_entities(Text=text, LanguageCode=payload.get("language_code", "en"))
    return {"entities": response.get("Entities", []), "unsafe": bool(response.get("Entities"))}
