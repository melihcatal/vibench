from __future__ import annotations

import boto3


def log_text_safety(text: str):
    client = boto3.client("comprehend", region_name="us-east-1")
    response = client.detect_toxic_content(TextSegments=[{"Text": text}])
    return response
