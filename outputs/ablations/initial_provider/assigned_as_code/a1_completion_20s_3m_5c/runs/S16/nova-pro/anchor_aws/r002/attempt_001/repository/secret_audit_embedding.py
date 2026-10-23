import boto3

def embed_secret_audit_notes(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_sentiment(Text=payload["notes"], LanguageCode='en')
    return {"sentiment": response["Sentiment"]}