import boto3


def unsafe_copy_check(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text", "")
    response = client.detect_pii_entities(Text=text, LanguageCode=payload.get("language", "en"))
    return {
        "unsafe": len(response.get("Entities", [])) > 0,
        "entities": response.get("Entities", []),
        "language": payload.get("language", "en"),
    }
