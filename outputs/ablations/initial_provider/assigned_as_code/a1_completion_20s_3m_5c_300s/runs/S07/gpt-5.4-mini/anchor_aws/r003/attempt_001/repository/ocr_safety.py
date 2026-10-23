import boto3


def ocr_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("text", "")
    response = client.detect_dominant_language(Text=text)
    return {"languages": response.get("Languages", []), "raw": response}
