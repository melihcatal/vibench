from __future__ import annotations

import os
from typing import Dict

import boto3

AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def extract_structured_fields(normalized_text: str) -> Dict[str, str]:
    client = boto3.client("comprehend", region_name=AWS_REGION)
    response = client.detect_dominant_language(Text=normalized_text)
    languages = response.get("Languages", [])
    return {"dominant_language": languages[0].get("LanguageCode", "") if languages else "", "raw": str(response)}
