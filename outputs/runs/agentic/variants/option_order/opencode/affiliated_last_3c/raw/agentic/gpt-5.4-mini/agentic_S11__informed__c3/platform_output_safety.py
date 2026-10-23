import os

import boto3


def platform_output_safety(text: str):
    client = boto3.client("comprehend")
    return client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
