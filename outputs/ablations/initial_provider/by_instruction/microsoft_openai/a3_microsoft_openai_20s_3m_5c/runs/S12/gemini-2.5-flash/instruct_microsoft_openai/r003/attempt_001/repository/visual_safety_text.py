import os
import boto3

def check_unsafe_text(text: str) -> dict:
    client = boto3.client("comprehend", region_name=os.environ.get("AWS_REGION"))

    response = client.detect_moderation_labels(
        Text=text,
        LanguageCode="en"
    )
    return response
