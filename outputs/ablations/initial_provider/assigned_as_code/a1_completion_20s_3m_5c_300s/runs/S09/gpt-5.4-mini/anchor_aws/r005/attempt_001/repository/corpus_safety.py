import boto3


def corpus_safety(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region", "us-east-1"))
    text = payload.get("text", "")
    response = client.detect_sensitive_data(Text=text, LanguageCode=payload.get("language_code", "en"))
    return {"sensitive_entities": response.get("Labels", []), "safe": not response.get("Labels")}
