from typing import Any, Dict

import boto3

from security_models import normalize_text


def check_payload_safety(text: str) -> Dict[str, Any]:
    client = boto3.client("comprehend")
    content = normalize_text(text)
    response = client.detect_toxic_content(TextSegments=[{"Text": content}])
    return {"provider": "aws-comprehend", "text": content, "safety": response}
