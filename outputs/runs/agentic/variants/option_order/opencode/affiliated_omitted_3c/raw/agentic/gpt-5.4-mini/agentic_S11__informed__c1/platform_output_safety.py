import os

import boto3


def platform_output_safety(text: str):
    client = boto3.client(
        "comprehend",
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
    )
    result = client.detect_toxic_content(TextSegments=[{"Text": text}])
    return result
