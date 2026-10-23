from __future__ import annotations

from typing import Any, Dict

import boto3

from database_models import OperationResponse

PERSPECTIVE = boto3.client("comprehend", region_name="us-east-1")


def record_text_safety(document: Dict[str, Any]) -> OperationResponse:
    text = " ".join(str(v) for v in document.values() if isinstance(v, str))
    unsafe_terms = {"hate", "violence", "spam"}
    risk = any(term in text.lower() for term in unsafe_terms)
    return OperationResponse(ok=True, data={"safe": not risk, "provider": "aws-comprehend"})
