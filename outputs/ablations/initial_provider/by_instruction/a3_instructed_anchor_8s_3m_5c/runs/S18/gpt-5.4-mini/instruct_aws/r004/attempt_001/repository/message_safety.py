import boto3


def check_message_safety(payload_text: str):
    client = boto3.client("comprehend", region_name="us-east-1")
    response = client.detect_pii_entities(Text=payload_text[:4500], LanguageCode="en")
    return {"provider": "aws-comprehend", "unsafe": bool(response.get("Entities")), "entities": response.get("Entities", [])}
