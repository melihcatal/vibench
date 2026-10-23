import boto3
import os
from typing import List, Dict

def script_safety(text: str) -> List[Dict]:
    comprehend_client = boto3.client(
        "comprehend",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    # Detects personally identifiable information (PII) entities
    response = comprehend_client.detect_pii_entities(Text=text, LanguageCode="en")
    return response["Entities"]
