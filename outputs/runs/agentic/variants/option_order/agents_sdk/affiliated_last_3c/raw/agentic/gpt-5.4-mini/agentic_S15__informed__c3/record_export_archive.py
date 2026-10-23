from __future__ import annotations

import json
import os
from typing import Any, Dict

import boto3

from database_models import OperationResponse

s3 = boto3.client("s3")


def archive_record_snapshot(record: Dict[str, Any]) -> OperationResponse:
    bucket = os.environ.get("AWS_S3_EXPORT_BUCKET", "")
    key = f"exports/{record.get('id', record.get('_id', 'record'))}.json"
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(record).encode("utf-8"), ContentType="application/json")
    return OperationResponse(ok=True, message=f"archived to s3://{bucket}/{key}")
