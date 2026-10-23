import os
import json
import gzip
from datetime import datetime
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError
from google.cloud import storage


def archive_metrics_to_gcs(
    metric_data: List[Dict[str, Any]], bucket_name: str, prefix: Optional[str] = None
) -> Dict[str, Any]:
    """
    Archive exported metric snapshots in Google Cloud Storage.

    Args:
        metric_data: List of metric datapoints to archive
        bucket_name: Google Cloud Storage bucket name
        prefix: Optional prefix for the object path

    Returns:
        Dictionary with archive results
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    storage_client = storage.Client(project=project_id)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    if prefix:
        object_name = f"{prefix}/metrics_export_{timestamp}.json.gz"
    else:
        object_name = f"metrics_export_{timestamp}.json.gz"

    try:
        bucket = storage_client.bucket(bucket_name)

        json_data = json.dumps(metric_data, default=str, indent=2)
        compressed_data = gzip.compress(json_data.encode("utf-8"))

        blob = bucket.blob(object_name)
        blob.upload_from_string(compressed_data, content_type="application/gzip")

        blob.acl.all().grant_read()
        blob.acl.save()

        result = {
            "success": True,
            "bucket": bucket_name,
            "object": object_name,
            "size_bytes": len(compressed_data),
            "original_size_bytes": len(json_data),
            "compression_ratio": len(json_data) / max(len(compressed_data), 1),
            "timestamp": timestamp,
            "datapoint_count": len(metric_data),
            "storage_class": blob.storage_class,
            "md5_hash": blob.md5_hash,
            "crc32c": blob.crc32c,
            "generation": blob.generation,
            "metageneration": blob.metageneration,
            "service": "Google Cloud Storage",
        }

    except Exception as e:
        result = {
            "success": False,
            "error": str(e),
            "bucket": bucket_name,
            "object": object_name,
            "timestamp": timestamp,
            "service": "Google Cloud Storage",
        }

    return result


def archive_metrics_to_s3(
    metric_data: List[Dict[str, Any]], bucket_name: str, prefix: Optional[str] = None
) -> Dict[str, Any]:
    """
    Archive exported metric snapshots in Amazon S3.

    Args:
        metric_data: List of metric datapoints to archive
        bucket_name: Amazon S3 bucket name
        prefix: Optional prefix for the object key

    Returns:
        Dictionary with archive results
    """
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    if prefix:
        object_key = f"{prefix}/metrics_export_{timestamp}.json.gz"
    else:
        object_key = f"metrics_export_{timestamp}.json.gz"

    try:
        json_data = json.dumps(metric_data, default=str, indent=2)
        compressed_data = gzip.compress(json_data.encode("utf-8"))

        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=compressed_data,
            ContentType="application/gzip",
            ContentEncoding="gzip",
            Metadata={
                "datapoint-count": str(len(metric_data)),
                "export-timestamp": timestamp,
                "compressed": "true",
            },
        )

        result = {
            "success": True,
            "bucket": bucket_name,
            "key": object_key,
            "size_bytes": len(compressed_data),
            "original_size_bytes": len(json_data),
            "compression_ratio": len(json_data) / max(len(compressed_data), 1),
            "timestamp": timestamp,
            "datapoint_count": len(metric_data),
            "etag": response["ETag"].strip('"'),
            "version_id": response.get("VersionId"),
            "storage_class": response.get("StorageClass", "STANDARD"),
            "service": "Amazon S3",
        }

    except ClientError as e:
        result = {
            "success": False,
            "error": str(e),
            "bucket": bucket_name,
            "key": object_key,
            "timestamp": timestamp,
            "service": "Amazon S3",
        }

    return result


def create_metrics_snapshot(
    metric_data: List[Dict[str, Any]], snapshot_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a comprehensive metrics snapshot with metadata.

    Args:
        metric_data: List of metric datapoints
        snapshot_name: Optional custom snapshot name

    Returns:
        Dictionary with snapshot data and metadata
    """
    if not metric_data:
        return {"success": False, "error": "No metric data provided", "snapshot": None}

    if not snapshot_name:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"metrics_snapshot_{timestamp}"

    metric_types = set()
    resource_types = set()
    timestamps = []
    values = []

    for point in metric_data:
        metric_types.add(point.get("metric_type", "unknown"))
        resource_types.add(point.get("resource_type", "unknown"))

        if "timestamp" in point:
            timestamps.append(point["timestamp"])

        if "value" in point and point["value"] is not None:
            values.append(point["value"])

    snapshot = {
        "metadata": {
            "snapshot_name": snapshot_name,
            "created_at": datetime.utcnow().isoformat(),
            "datapoint_count": len(metric_data),
            "metric_types": list(metric_types),
            "resource_types": list(resource_types),
            "time_range": {
                "start": min(timestamps).isoformat() if timestamps else None,
                "end": max(timestamps).isoformat() if timestamps else None,
            }
            if timestamps
            else None,
            "value_statistics": {
                "count": len(values),
                "min": min(values) if values else None,
                "max": max(values) if values else None,
                "mean": sum(values) / len(values) if values else None,
            }
            if values
            else None,
        },
        "data": metric_data,
    }

    return {"success": True, "snapshot": snapshot, "snapshot_name": snapshot_name}


def archive_snapshot_to_both_providers(
    metric_data: List[Dict[str, Any]],
    gcs_bucket: Optional[str] = None,
    s3_bucket: Optional[str] = None,
    prefix: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive metrics snapshot to both Google Cloud Storage and Amazon S3.

    Args:
        metric_data: List of metric datapoints
        gcs_bucket: Google Cloud Storage bucket name (optional)
        s3_bucket: Amazon S3 bucket name (optional)
        prefix: Optional prefix for object paths

    Returns:
        Dictionary with archive results from both providers
    """
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "datapoint_count": len(metric_data),
        "archives": {},
    }

    snapshot_result = create_metrics_snapshot(metric_data)
    results["snapshot"] = snapshot_result

    if gcs_bucket and snapshot_result["success"]:
        gcs_result = archive_metrics_to_gcs(
            snapshot_result["snapshot"]["data"], gcs_bucket, prefix
        )
        results["archives"]["gcs"] = gcs_result

    if s3_bucket and snapshot_result["success"]:
        s3_result = archive_metrics_to_s3(
            snapshot_result["snapshot"]["data"], s3_bucket, prefix
        )
        results["archives"]["s3"] = s3_result

    results["success"] = any(
        archive.get("success", False) for archive in results["archives"].values()
    )

    return results


if __name__ == "__main__":
    sample_metrics = [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "value": 0.75,
            "metric_type": "compute.googleapis.com/instance/cpu/utilization",
            "resource_type": "gce_instance",
            "resource_labels": {"instance_id": "test-1", "zone": "us-central1-a"},
        },
        {
            "timestamp": (datetime.utcnow()).isoformat(),
            "value": 0.82,
            "metric_type": "compute.googleapis.com/instance/cpu/utilization",
            "resource_type": "gce_instance",
            "resource_labels": {"instance_id": "test-2", "zone": "us-central1-b"},
        },
    ]

    try:
        snapshot = create_metrics_snapshot(sample_metrics)
        print(f"Created snapshot: {snapshot['snapshot_name']}")
        print(f"Datapoints: {snapshot['snapshot']['metadata']['datapoint_count']}")
        print(f"Metric types: {snapshot['snapshot']['metadata']['metric_types']}")

    except Exception as e:
        print(f"Error creating metrics snapshot: {e}")
