import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _s3_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return boto3.client("s3", region_name=region)


def archive_record_export(
    export_payload: Dict[str, Any],
    bucket: str,
    key_prefix: str = "exports",
    s3_client: Optional[Any] = None,
) -> Dict[str, Any]:
    client = s3_client or _s3_client()
    record_id = str(
        export_payload.get("id")
        or export_payload.get("document_id")
        or export_payload.get("record_id")
        or "unknown"
    )
    archive_key = f"{key_prefix.rstrip('/')}/{record_id}.json"
    body = json.dumps(export_payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    try:
        response = client.put_object(
            Bucket=bucket,
            Key=archive_key,
            Body=body,
            ContentType="application/json",
        )
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"Failed to archive export to s3://{bucket}/{archive_key}") from exc
    return {
        "bucket": bucket,
        "key": archive_key,
        "etag": response.get("ETag"),
        "version_id": response.get("VersionId"),
    }
