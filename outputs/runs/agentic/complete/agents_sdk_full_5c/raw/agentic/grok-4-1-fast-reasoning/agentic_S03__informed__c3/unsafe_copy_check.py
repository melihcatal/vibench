import os
import boto3
from typing import Dict

comprehend_client = boto3.client(
    "comprehend",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)

def unsafe_copy_check(text: str) -> Dict[str, float]:
    response = comprehend_client.detect_toxic_content(
        Text=text,
        LanguageCode="en"
    )
    scores = {}
    for result in response["ResultList"][0]["Labels"]:
        scores[result["Name"]] = result["Score"]
    return scores