import boto3
import os
from typing import List, Dict, Any

def script_safety(text: str) -> List[Dict[str, Any]]:
    """
    Checks narration scripts for unsafe content using AWS Comprehend.
    """
    comprehend_client = boto3.client(
        "comprehend",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    # Example: Detect PII. Comprehend offers other safety features too.
    response = comprehend_client.detect_pii_entities(Text=text, LanguageCode='en')

    return response['Entities']
