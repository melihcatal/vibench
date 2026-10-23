import boto3


def moderate_transcript(text: str) -> dict:
    client = boto3.client("comprehend")
    response = client.detect_pii_entities(Text=text, LanguageCode="en")
    return response
