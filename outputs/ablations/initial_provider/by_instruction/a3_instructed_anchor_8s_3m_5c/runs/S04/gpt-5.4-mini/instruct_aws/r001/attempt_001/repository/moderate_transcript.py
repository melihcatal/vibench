import boto3

from speech_client import get_aws_region


def moderate_transcript(text: str):
    client = boto3.client("comprehend", region_name=get_aws_region())
    return client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
