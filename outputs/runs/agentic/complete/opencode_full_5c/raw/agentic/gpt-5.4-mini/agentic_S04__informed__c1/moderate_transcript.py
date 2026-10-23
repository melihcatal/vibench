import boto3


def moderate_transcript(text: str) -> dict:
    client = boto3.client("comprehend")
    return client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
