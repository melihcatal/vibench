import boto3


def metric_annotation_safety(payload, config=None):
    comprehend = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text", "")
    response = comprehend.detect_dominant_language(Text=text[:5000])
    languages = response.get("Languages", [])
    unsafe = any(item.get("LanguageCode") not in {"en", "es", "fr", "de", "pt", "it", "ja", "ko", "zh"} for item in languages)
    return {"text": text, "languages": languages, "unsafe": unsafe}
