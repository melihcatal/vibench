import boto3


def moderate_transcript(text, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    
    # Example moderation: Detect PII entities
    response = client.detect_pii_entities(Text=text, LanguageCode="en")
    
    # You can extend this to include sentiment analysis, key phrase extraction, etc.
    # For simplicity, we just return the PII entities found.
    return response["Entities"]
