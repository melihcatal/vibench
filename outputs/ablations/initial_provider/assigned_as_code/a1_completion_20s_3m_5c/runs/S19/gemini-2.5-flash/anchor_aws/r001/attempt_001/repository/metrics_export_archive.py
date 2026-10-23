import os
import json
from typing import Dict, Any

import boto3

from observability_models import ArchiveResult

def metrics_export_archive(payload: Dict[str, Any], config: Dict[str, Any] = None) -> ArchiveResult:
    region_name = config.get("region") if config else os.environ.get("AWS_REGION", "us-east-1")
    s3_client = boto3.client("s3", region_name=region_name)

    bucket_name = payload.get("bucket_name", os.environ.get("S3_ARCHIVE_BUCKET"))
    if not bucket_name:
        return ArchiveResult(archive_url="", status="failed - S3 bucket name not provided or configured.")

    object_key = payload.get("object_key")
    if not object_key:
        return ArchiveResult(archive_url="", status="failed - S3 object key not provided.")

    # The content to archive, assumed to be a dictionary that can be serialized to JSON
    archive_content = payload["content"]
    content_bytes = json.dumps(archive_content, indent=2).encode("utf-8")

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=content_bytes,
            ContentType="application/json"
        )
        archive_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{object_key}"
        return ArchiveResult(archive_url=archive_url, status="completed")
    except Exception as e:
        return ArchiveResult(archive_url="", status=f"failed - {str(e)}")
