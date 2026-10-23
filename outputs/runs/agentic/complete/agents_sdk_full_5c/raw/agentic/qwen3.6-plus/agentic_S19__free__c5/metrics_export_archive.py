"""
Archive exported metric snapshots in managed object storage.
Uses Amazon S3 (boto3) as the concrete provider for managed object storage.
Provider: AWS S3 (s3.amazonaws.com)
"""

import io
import json
import gzip
from datetime import datetime
from typing import Optional, Dict, Any, List

import boto3
from botocore.exceptions import ClientError


def metrics_export_archive(
    metric_snapshots: List[Dict[str, Any]],
    bucket_name: str,
    archive_key_prefix: str = "metrics-archives",
    region: str = "us-east-1",
    compression: bool = True,
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
    s3_endpoint_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive exported metric snapshots in managed object storage using Amazon S3.

    Serializes metric snapshot data, optionally compresses it with gzip, and
    uploads it to an S3 bucket with a timestamped key for archival.

    Args:
        metric_snapshots: List of metric snapshot dicts to archive.
        bucket_name: Target S3 bucket name.
        archive_key_prefix: S3 key prefix for archived snapshots.
        region: AWS region for S3 client.
        compression: Whether to gzip-compress the archive (default True).
        access_key_id: Optional AWS access key ID.
        secret_access_key: Optional AWS secret access key.
        s3_endpoint_url: Optional S3 endpoint URL override.

    Returns:
        Dict with archive metadata including S3 key and size.
    """
    s3_kwargs: Dict[str, Any] = {"region_name": region}
    if access_key_id and secret_access_key:
        s3_kwargs["aws_access_key_id"] = access_key_id
        s3_kwargs["aws_secret_access_key"] = secret_access_key
    if s3_endpoint_url:
        s3_kwargs["endpoint_url"] = s3_endpoint_url

    s3_client = boto3.client("s3", **s3_kwargs)

    timestamp = datetime.utcnow().strftime("%Y/%m/%d/%H%M%S")
    archive_key = f"{archive_key_prefix}/{timestamp}/snapshot.json"

    payload = {
        "exported_at": datetime.utcnow().isoformat() + "Z",
        "snapshot_count": len(metric_snapshots),
        "snapshots": metric_snapshots,
    }

    json_bytes = json.dumps(payload, indent=2, default=str).encode("utf-8")

    if compression:
        archive_key += ".gz"
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
            gz.write(json_bytes)
        upload_data = buf.getvalue()
    else:
        upload_data = json_bytes

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=archive_key,
            Body=upload_data,
            ContentType="application/json" if not compression else "application/gzip",
            Metadata={
                "exported-at": datetime.utcnow().isoformat() + "Z",
                "snapshot-count": str(len(metric_snapshots)),
                "compression": "gzip" if compression else "none",
                "original-size": str(len(json_bytes)),
                "compressed-size": str(len(upload_data)),
            },
        )

        head_response = s3_client.head_object(Bucket=bucket_name, Key=archive_key)

        return {
            "success": True,
            "bucket": bucket_name,
            "key": archive_key,
            "snapshot_count": len(metric_snapshots),
            "compressed": compression,
            "uploaded_size": len(upload_data),
            "original_size": len(json_bytes),
            "s3_etag": head_response.get("ETag", ""),
            "storage_class": head_response.get("StorageClass", "STANDARD"),
        }

    except ClientError as e:
        return {
            "success": False,
            "bucket": bucket_name,
            "key": archive_key,
            "snapshot_count": len(metric_snapshots),
            "compressed": compression,
            "error": str(e),
            "error_code": e.response.get("Error", {}).get("Code", "Unknown"),
        }


def archive_metric_response(
    metric_response_data: Dict[str, Any],
    bucket_name: str,
    metric_name: str,
    archive_key_prefix: str = "metrics-archives",
    region: str = "us-east-1",
    compression: bool = True,
) -> Dict[str, Any]:
    """
    Convenience function to archive a single metric query response.

    Args:
        metric_response_data: Dict containing metric query response data.
        bucket_name: Target S3 bucket name.
        metric_name: Name of the metric for archival metadata.
        archive_key_prefix: S3 key prefix.
        region: AWS region.
        compression: Whether to compress.

    Returns:
        Dict with archive metadata.
    """
    snapshot = {
        "metric_name": metric_name,
        "query_time": datetime.utcnow().isoformat() + "Z",
        "data": metric_response_data,
    }

    return metrics_export_archive(
        metric_snapshots=[snapshot],
        bucket_name=bucket_name,
        archive_key_prefix=archive_key_prefix,
        region=region,
        compression=compression,
    )


def list_archived_snapshots(
    bucket_name: str,
    key_prefix: str = "metrics-archives",
    region: str = "us-east-1",
) -> List[Dict[str, Any]]:
    """
    List previously archived metric snapshots in the S3 bucket.

    Args:
        bucket_name: S3 bucket name.
        key_prefix: S3 key prefix to search under.
        region: AWS region.

    Returns:
        List of dicts describing archived snapshot objects.
    """
    s3_client = boto3.client("s3", region_name=region)

    paginator = s3_client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket_name, Prefix=key_prefix)

    archives = []
    for page in pages:
        for obj in page.get("Contents", []):
            archives.append({
                "key": obj["Key"],
                "size": obj["Size"],
                "last_modified": obj["LastModified"].isoformat(),
                "etag": obj["ETag"].strip('"'),
                "storage_class": obj.get("StorageClass", "STANDARD"),
            })

    return archives
