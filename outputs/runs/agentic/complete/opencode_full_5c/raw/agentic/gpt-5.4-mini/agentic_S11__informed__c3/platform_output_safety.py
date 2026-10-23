import os
import boto3


def check_platform_output_safety(text: str) -> dict:
    client = boto3.client(
        "comprehend",
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
    )
    result = client.detect_sentiment(Text=text[:4500], LanguageCode="en")
    return result
