import boto3


def payload_safety(payload, config=None):
    config = config or {}
    comprehend = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("plaintext", b"")
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="ignore")
    response = comprehend.detect_dominant_language(Text=text[:5000])
    languages = response.get("Languages", [])
    unsafe = any(lang.get("LanguageCode") not in {"en", "es", "fr", "de"} for lang in languages)
    return {"unsafe": unsafe, "languages": languages}
