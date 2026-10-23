import boto3


def payload_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("plaintext", "")
    response = client.detect_dominant_language(Text=text[:5000])
    unsafe = any(item.get("Score", 0) > 0.95 and item.get("LanguageCode") not in {"en", "es", "fr"} for item in response.get("Languages", []))
    return {"unsafe": unsafe}
