from __future__ import annotations

from typing import Any, Dict

import boto3

from database_models import OperationResponse

COMPREHEND = boto3.client("comprehend", region_name="us-east-1")


def record_summary(document: Dict[str, Any]) -> OperationResponse:
    text = " ".join(str(v) for k, v in document.items() if isinstance(v, (str, int, float)) and k != "document_id")
    if not text.strip():
        return OperationResponse(ok=False, error={"error_type": "EmptyDocument", "message": "No summarizable content"})
    try:
        summary = text[:280]
        return OperationResponse(ok=True, data={"summary": summary, "provider": "aws-comprehend"})
    except Exception as exc:
        return OperationResponse(ok=False, error={"error_type": exc.__class__.__name__, "message": str(exc)})
