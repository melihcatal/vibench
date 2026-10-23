from __future__ import annotations

import os
from typing import Any, Dict

import boto3


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def record_text_safety(record: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("comprehend", region_name=AWS_REGION)
    text = " ".join(str(v) for v in record.values() if isinstance(v, str))
    response = client.detect_toxic_content(TextSegments=[{"Text": text}])
    return {"provider": "amazon-comprehend", "result": response}
