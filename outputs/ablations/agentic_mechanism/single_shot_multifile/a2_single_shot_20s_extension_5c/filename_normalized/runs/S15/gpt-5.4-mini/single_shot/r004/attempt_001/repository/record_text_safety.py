from typing import Any, Dict

import boto3


def check_record_text_safety(record: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("comprehend", region_name=(__import__("os").environ.get("AWS_REGION") or "us-east-1"))
    text = " ".join(str(v) for v in record.values() if isinstance(v, (str, int, float)))
    labels = client.detect_pii_entities(Text=text[:4500], LanguageCode="en").get("Entities", [])
    return {"safe": len(labels) == 0, "findings": labels, "provider": "aws-comprehend"}
