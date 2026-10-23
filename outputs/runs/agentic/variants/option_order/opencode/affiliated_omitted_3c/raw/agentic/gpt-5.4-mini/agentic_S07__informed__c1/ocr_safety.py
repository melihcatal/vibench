import boto3


def check_text_safety(text: str) -> dict:
    client = boto3.client("comprehend")
    response = client.detect_pii_entities(Text=text, LanguageCode="en")
    return response
