import os
import json
import gzip
from datetime import datetime, timezone
from typing import Optional
import io

import boto3
from botocore.exceptions import ClientError


def _get_s3_client() -> boto3.client:
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required for Amazon S3"
        )
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )


def archive_metric_snapshot(
    bucket: str,
    key: str,
    snapshot_data: dict,
    compress: bool = True,
    metadata: Optional[dict] = None,
) -> dict:
    s3_client = _get_s3_client()

    if compress:
        body = gzip.compress(json.dumps(snapshot_data, default=str).encode("utf-8"))
        content_encoding = "gzip"
        content_type = "application/json"
    else:
        body = json.dumps(snapshot_data, default=str).encode("utf-8")
        content_encoding = None
        content_type = "application/json"

    upload_kwargs = {
        "Bucket": bucket,
        "Key": key,
        "Body": body,
        "ContentType": content_type,
    }
    if content_encoding:
        upload_kwargs["ContentEncoding"] = content_encoding
    if metadata:
        upload_kwargs["Metadata"] = metadata

    response = s3_client.put_object(**upload_kwargs)

    return {
        "bucket": bucket,
        "key": key,
        "etag": response.get("ETag", "").strip('"'),
        "version_id": response.get("VersionId"),
        "compressed": compress,
        "size_bytes": len(body),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "Amazon S3",
    }


def archive_metric_snapshots_batch(
    bucket: str,
    prefix: str,
    snapshots: list[dict],
    compress: bool = True,
) -> list[dict]:
    results = []
    for i, snapshot in enumerate(snapshots):
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        key = f"{prefix}/snapshot_{timestamp}_{i:04d}.json"
        result = archive_metric_snapshot(
            bucket=bucket,
            key=key,
            snapshot_data=snapshot,
            compress=compress,
            metadata={"index": str(i), "total": str(len(snapshots))},
        )
        results.append(result)
    return results


def retrieve_archived_snapshot(
    bucket: str,
    key: str,
    decompress: bool = True,
) -> dict:
    s3_client = _get_s3_client()

    response = s3_client.get_object(Bucket=bucket, Key=key)
    body = response["Body"].read()

    if decompress and response.get("ContentEncoding") == "gzip":
        body = gzip.decompress(body)

    data = json.loads(body.decode("utf-8"))
    return {
        "data": data,
        "key": key,
        "bucket": bucket,
        "last_modified": response.get("LastModified").isoformat()
        if response.get("LastModified")
        else None,
        "content_length": response.get("ContentLength"),
        "service": "Amazon S3",
    }


def list_archived_snapshots(
    bucket: str,
    prefix: str = "",
    max_keys: int = 100,
) -> list[dict]:
    s3_client = _get_s3_client()

    response = s3_client.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix,
        MaxKeys=max_keys,
    )

    objects = response.get("Contents", [])
    return [
        {
            "key": obj["Key"],
            "size": obj["Size"],
            "last_modified": obj["LastModified"].isoformat()
            if obj.get("LastModified")
            else None,
            "etag": obj.get("ETag", "").strip('"'),
        }
        for obj in objects
    ]
