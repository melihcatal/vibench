import boto3


def record_summary(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text") or payload.get("document", {}).get("text", "")
    response = client.detect_key_phrases(Text=text[:4500], LanguageCode=payload.get("language", "en"))
    phrases = [phrase["Text"] for phrase in response.get("KeyPhrases", [])]
    return {"summary": ", ".join(phrases[:5])}
