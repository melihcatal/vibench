import boto3


def payload_safety(payload, config=None):
    config = config or {}
    comprehend = boto3.client("comprehend", region_name=config.get("region"))
    response = comprehend.detect_dominant_language(Text=payload["text"])
    languages = response.get("Languages", [])
    unsafe = any(item.get("Score", 0.0) < 0.5 for item in languages)
    return {"unsafe": unsafe, "languages": languages}
