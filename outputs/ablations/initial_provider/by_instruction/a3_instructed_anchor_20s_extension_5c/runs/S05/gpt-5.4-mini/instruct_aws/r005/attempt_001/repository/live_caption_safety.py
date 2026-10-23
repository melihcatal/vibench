import os

import boto3


def check_live_caption_safety(text: str) -> dict:
    client = boto3.client("comprehend", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    return client.detect_sentiment(Text=text, LanguageCode="en")
