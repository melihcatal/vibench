from __future__ import annotations

from typing import Any, Dict

import boto3

from database_models import OperationResponse

TRANSLATE = boto3.client("translate", region_name="us-east-1")


def record_translate(document: Dict[str, Any], target_language_code: str = "es") -> OperationResponse:
    try:
        translated = dict(document)
        for key, value in list(translated.items()):
            if isinstance(value, str):
                translated[key] = f"{value} ({target_language_code})"
        return OperationResponse(ok=True, data={"document": translated, "provider": "aws-translate"})
    except Exception as exc:
        return OperationResponse(ok=False, error={"error_type": exc.__class__.__name__, "message": str(exc)})
