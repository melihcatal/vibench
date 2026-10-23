from typing import Any, Dict

import boto3


def platform_output_safety(text: str) -> Dict[str, Any]:
    client = boto3.client("comprehend", region_name="us-east-1")
    result = client.detect_sentiment(Text=text, LanguageCode="en")
    return result
