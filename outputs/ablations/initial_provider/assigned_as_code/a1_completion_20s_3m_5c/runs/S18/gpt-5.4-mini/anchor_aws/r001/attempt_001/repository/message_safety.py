import boto3


def message_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_pii_entities(Text=payload["text"], LanguageCode=payload.get("language", "en"))
    unsafe = [item["Type"] for item in response.get("Entities", [])]
    return {"unsafe": bool(unsafe), "unsafe_types": unsafe}
