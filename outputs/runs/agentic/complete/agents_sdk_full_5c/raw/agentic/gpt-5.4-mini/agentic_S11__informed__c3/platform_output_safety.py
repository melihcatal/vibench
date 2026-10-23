from __future__ import annotations

from typing import Any, Dict

import boto3



def check_platform_output_safety(text: str) -> Dict[str, Any]:
    client = boto3.client("comprehend")
    result = client.detect_toxic_content(TextSegments=[{"Text": text}])
    return {"provider": "Amazon Comprehend", "toxicity": result}
