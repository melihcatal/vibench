from typing import Any, Dict

import boto3


def record_export_archive(bucket: str, key: str, body: bytes) -> Dict[str, Any]:
    client = boto3.client("s3")
    response = client.put_object(Bucket=bucket, Key=key, Body=body)
    return {
        "etag": response.get("ETag", ""),
        "version_id": response.get("VersionId", ""),
    }
