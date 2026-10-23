"""
Archive exported metric snapshots in managed object storage.

Uses AWS S3 (Simple Storage Service) to store metric data snapshots as managed
object storage archives.

Provider signals:
  - boto3 S3 client
  - AWS S3 bucket operations (put_object, list_objects_v2)
  - S3 storage classes (STANDARD_IA, GLACIER)
  - AWS S3 endpoint URL
"""

import json
import gzip
import io
from datetime import datetime
from typing import Any, Dict, List, Optional

import boto3
from botocore.config import Config

from observability_client import AWS_REGION
from observability_models import MetricDataPoint


S3_STORAGE_CLASS_STANDARD_IA = "STANDARD_IA"
S3_STORAGE_CLASS_GLACIER = "GLACIER"
S3_STORAGE_CLASS_INTELLIGENT_TIERING = "INTELLIGENT_TIERING"


def _create_s3_client():
    """Create a boto3 S3 client."""
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
    )
    session = boto3.Session(region_name=AWS_REGION)
    return session.client("s3", config=config)


class ArchiveMetadata:
    """Metadata for an archived metric snapshot."""

    def __init__(
        self,
        bucket: str,
        object_key: str,
        metric_name: str,
        namespace: str,
        archive_time: datetime,
        data_point_count: int,
        file_size_bytes: int,
        storage_class: str,
        snapshot_start: datetime,
        snapshot_end: datetime,
    ):
        self.bucket = bucket
        self.object_key = object_key
        self.metric_name = metric_name
        self.namespace = namespace
        self.archive_time = archive_time
        self.data_point_count = data_point_count
        self.file_size_bytes = file_size_bytes
        self.storage_class = storage_class
        self.snapshot_start = snapshot_start
        self.snapshot_end = snapshot_end

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bucket": self.bucket,
            "object_key": self.object_key,
            "metric_name": self.metric_name,
            "namespace": self.namespace,
            "archive_time": self.archive_time.isoformat(),
            "data_point_count": self.data_point_count,
            "file_size_bytes": self.file_size_bytes,
            "storage_class": self.storage_class,
            "snapshot_start": self.snapshot_start.isoformat(),
            "snapshot_end": self.snapshot_end.isoformat(),
        }


def _build_s3_object_key(
    metric_name: str,
    namespace: str,
    snapshot_time: datetime,
    dimensions: Optional[Dict[str, str]] = None,
) -> str:
    """Build a structured S3 object key for metric archive."""
    ts = snapshot_time.strftime("%Y/%m/%d/%H%M%S")
    ns_path = namespace.replace("/", "_")
    base_key = f"metrics-archive/{ns_path}/{metric_name}/{ts}/snapshot.json.gz"
    return base_key


def metrics_export_archive(
    bucket: str,
    metric_name: str,
    namespace: str,
    datapoints: List[MetricDataPoint],
    snapshot_start: datetime,
    snapshot_end: datetime,
    storage_class: str = S3_STORAGE_CLASS_STANDARD_IA,
    dimensions: Optional[Dict[str, str]] = None,
    archive_metadata: Optional[Dict[str, str]] = None,
) -> ArchiveMetadata:
    """
    Export and archive metric snapshots to AWS S3 managed object storage.

    Serializes metric datapoints as compressed JSON and uploads to S3 with
    structured key paths and optional lifecycle storage class.

    Args:
        bucket: Target S3 bucket name
        metric_name: CloudWatch metric name being archived
        namespace: CloudWatch namespace
        datapoints: List of MetricDataPoint objects to archive
        snapshot_start: Start of the snapshot window
        snapshot_end: End of the snapshot window
        storage_class: S3 storage class (STANDARD_IA, GLACIER, INTELLIGENT_TIERING)
        dimensions: Optional dimension filters that were applied
        archive_metadata: Additional metadata to include in the archive manifest

    Returns:
        ArchiveMetadata with S3 object details.
    """
    s3 = _create_s3_client()

    archive_time = datetime.utcnow()
    object_key = _build_s3_object_key(metric_name, namespace, archive_time, dimensions)

    serializable_points = []
    for dp in datapoints:
        point_dict = {
            "timestamp": dp.timestamp.isoformat() if dp.timestamp else None,
            "value": dp.value,
            "unit": dp.unit,
            "sample_count": dp.sample_count,
        }
        serializable_points.append(point_dict)

    manifest = {
        "archive_metadata": {
            "metric_name": metric_name,
            "namespace": namespace,
            "snapshot_start": snapshot_start.isoformat(),
            "snapshot_end": snapshot_end.isoformat(),
            "archive_time": archive_time.isoformat(),
            "datapoint_count": len(serializable_points),
            "storage_class": storage_class,
        },
        "dimensions": dimensions or {},
        "custom_metadata": archive_metadata or {},
        "datapoints": serializable_points,
    }

    json_bytes = json.dumps(manifest, indent=2).encode("utf-8")

    compressed = io.BytesIO()
    with gzip.GzipFile(fileobj=compressed, mode="wb") as gz:
        gz.write(json_bytes)
    compressed.seek(0)
    gz_data = compressed.read()

    s3_params = {
        "Bucket": bucket,
        "Key": object_key,
        "Body": gz_data,
        "ContentType": "application/gzip",
        "ContentEncoding": "gzip",
        "StorageClass": storage_class,
        "Metadata": {
            "metric-name": metric_name,
            "namespace": namespace.replace("/", "_"),
            "snapshot-start": snapshot_start.strftime("%Y%m%dT%H%M%SZ"),
            "snapshot-end": snapshot_end.strftime("%Y%m%dT%H%M%SZ"),
        },
    }

    response = s3.put_object(**s3_params)

    return ArchiveMetadata(
        bucket=bucket,
        object_key=object_key,
        metric_name=metric_name,
        namespace=namespace,
        archive_time=archive_time,
        data_point_count=len(datapoints),
        file_size_bytes=len(gz_data),
        storage_class=storage_class,
        snapshot_start=snapshot_start,
        snapshot_end=snapshot_end,
    )


def metrics_export_archive_batch(
    bucket: str,
    metric_snapshots: List[Dict[str, Any]],
    storage_class: str = S3_STORAGE_CLASS_STANDARD_IA,
) -> List[ArchiveMetadata]:
    """
    Batch archive multiple metric snapshots to AWS S3.

    Args:
        bucket: Target S3 bucket name
        metric_snapshots: List of dicts containing metric_name, namespace,
                          datapoints, snapshot_start, snapshot_end
        storage_class: S3 storage class

    Returns:
        List of ArchiveMetadata objects.
    """
    results = []
    for snapshot in metric_snapshots:
        metadata = metrics_export_archive(
            bucket=bucket,
            metric_name=snapshot["metric_name"],
            namespace=snapshot["namespace"],
            datapoints=snapshot.get("datapoints", []),
            snapshot_start=snapshot["snapshot_start"],
            snapshot_end=snapshot["snapshot_end"],
            storage_class=storage_class,
            dimensions=snapshot.get("dimensions"),
            archive_metadata=snapshot.get("archive_metadata"),
        )
        results.append(metadata)
    return results


def list_metric_archives(
    bucket: str,
    metric_name: Optional[str] = None,
    namespace: Optional[str] = None,
    prefix: str = "metrics-archive/",
) -> List[Dict[str, Any]]:
    """
    List archived metric snapshots from S3.

    Args:
        bucket: S3 bucket name
        metric_name: Optional metric name filter
        namespace: Optional namespace filter
        prefix: S3 key prefix

    Returns:
        List of S3 object metadata dicts.
    """
    s3 = _create_s3_client()

    params = {
        "Bucket": bucket,
        "Prefix": prefix,
    }

    response = s3.list_objects_v2(**params)
    objects = response.get("Contents", [])

    archives = []
    for obj in objects:
        key = obj.get("Key", "")
        if metric_name and metric_name not in key:
            continue
        if namespace and namespace.replace("/", "_") not in key:
            continue
        archives.append({
            "key": key,
            "size_bytes": obj.get("Size", 0),
            "last_modified": obj.get("LastModified"),
            "storage_class": obj.get("StorageClass"),
        })

    return archives


def retrieve_metric_archive(
    bucket: str,
    object_key: str,
) -> Dict[str, Any]:
    """
    Retrieve and decompress a metric archive from S3.

    Args:
        bucket: S3 bucket name
        object_key: S3 object key

    Returns:
        Parsed archive manifest as a dict.
    """
    s3 = _create_s3_client()

    response = s3.get_object(Bucket=bucket, Key=object_key)
    gz_data = response["Body"].read()

    with gzip.GzipFile(fileobj=io.BytesIO(gz_data), mode="rb") as gz:
        json_bytes = gz.read()

    manifest = json.loads(json_bytes.decode("utf-8"))
    return manifest
