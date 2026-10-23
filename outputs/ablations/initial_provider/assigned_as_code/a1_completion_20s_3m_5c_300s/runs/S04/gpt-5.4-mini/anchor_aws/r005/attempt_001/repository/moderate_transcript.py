import boto3


def moderate_transcript(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text") or " ".join(segment.get("text", "") for segment in payload.get("segments", []))
    response = client.detect_dominant_language(Text=text)
    languages = response.get("Languages", [])
    return {"approved": bool(text), "dominant_language": languages[0]["LanguageCode"] if languages else None, "text": text}
