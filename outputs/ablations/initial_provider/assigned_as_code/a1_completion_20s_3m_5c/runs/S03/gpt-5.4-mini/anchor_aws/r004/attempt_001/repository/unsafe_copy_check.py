import boto3


def unsafe_copy_check(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload["text"]
    response = client.detect_pii_entities(Text=text, LanguageCode=config.get("language", "en"))
    return {
        "text": text,
        "unsafe": bool(response.get("Entities")),
        "entities": response.get("Entities", []),
    }
