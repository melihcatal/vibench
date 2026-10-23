import boto3


def moderate_claim_text(text: str) -> dict:
    client = boto3.client("comprehend")
    result = client.detect_pii_entities(Text=text, LanguageCode="en")
    return {"provider": "AWS Comprehend", "entities": result.get("Entities", [])}
