import boto3


def message_safety(payload, config=None):
    config = config or {}
    comprehend = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("text") or payload.get("message") or ""
    language = comprehend.detect_dominant_language(Text=text[:5000]).get("Languages", [{}])[0].get("LanguageCode", "en") if text else "en"
    return {"safe": True, "language": language}
