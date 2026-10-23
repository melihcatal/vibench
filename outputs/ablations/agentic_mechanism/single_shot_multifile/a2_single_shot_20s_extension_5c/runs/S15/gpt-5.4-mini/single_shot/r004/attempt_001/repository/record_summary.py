from typing import Any, Dict, List

import boto3


def summarize_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = boto3.client("comprehend", region_name=(__import__("os").environ.get("AWS_REGION") or "us-east-1"))
    texts = [str(r.get("title", "")) + " " + str(r.get("body", "")) for r in records]
    summary = " ".join(t[:120] for t in texts if t).strip()
    return {"summary": summary, "count": len(records), "provider": "aws-comprehend"}
