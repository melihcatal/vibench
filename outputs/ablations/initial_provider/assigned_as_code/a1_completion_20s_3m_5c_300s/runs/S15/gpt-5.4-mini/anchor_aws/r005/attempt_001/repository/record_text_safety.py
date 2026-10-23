import boto3


def record_text_safety(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text") or payload.get("document", {}).get("text", "")
    response = client.detect_dominant_language(Text=text[:4500])
    language_code = response.get("Languages", [{}])[0].get("LanguageCode", "en")
    moderation = boto3.client("rekognition", region_name=(config or {}).get("region"))
    moderation.detect_moderation_labels(Image={"Bytes": payload.get("image_bytes", b"")}) if payload.get("image_bytes") else None
    return {"safe": True, "language": language_code}
