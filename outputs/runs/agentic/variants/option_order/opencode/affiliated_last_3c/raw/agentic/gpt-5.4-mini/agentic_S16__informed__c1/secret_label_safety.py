import os

import boto3


def secret_label_safety(text: str) -> str:
    client = boto3.client("comprehend", region_name=os.getenv("AWS_REGION"))
    result = client.detect_dominant_language(Text=text)
    return result.get("Languages", [{}])[0].get("LanguageCode", "und")
