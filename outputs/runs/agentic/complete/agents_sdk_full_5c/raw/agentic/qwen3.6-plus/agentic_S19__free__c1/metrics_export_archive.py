"""
Archive exported metric snapshots in managed object storage using AWS S3.

Exports metric data snapshots and archives them to AWS S3 (s3.amazonaws.com)
for long-term retention, compliance, or cross-account sharing. Supports
JSON and CSV export formats with configurable storage classes.
"""

import os
import io
import json
import csv
import gzip
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, BinaryIO

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


# Provider-specific: AWS S3 endpoint and storage class identifiers
AWS_S3_ENDPOINT = "s3.amazonaws.com"
DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# AWS S3 storage class identifiers
S3_STORAGE_CLASSES = [
    "STANDARD",
    "STANDARD_IA",
    "ONEZONE_IA",
    "INTELLIGENT_TIERING",
    "GLACIER",
    "DEEP_ARCHIVE",
]

# Export format identifiers
EXPORT_FORMATS = ["json", "csv", "json_gzip", "csv_gzip"]


class ExportMetadata:
    """Metadata for an archived metric snapshot."""

    def __init__(
        self,
        bucket: str,
        key: str,
        metric_name: str,
        namespace: str,
        export_format: str,
        datapoint_count: int,
        start_time: datetime,
        end_time: datetime,
        storage_class: str,
        file_size_bytes: int,
        exported_at: datetime,
        etag: Optional[str] = None,
    ):
        self.bucket = bucket
        self.key = key
        self.metric_name = metric_name
        self.namespace = namespace
        self.export_format = export_format
        self.datapoint_count = datapoint_count
        self.start_time = start_time
        self.end_time = end_time
        self.storage_class = storage_class
        self.file_size_bytes = file_size_bytes
        self.exported_at = exported_at
        self.etag = etag

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bucket": self.bucket,
            "key": self.key,
            "s3_uri": f"s3://{self.bucket}/{self.key}",
            "metric_name": self.metric_name,
            "namespace": self.namespace,
            "export_format": self.export_format,
            "datapoint_count": self.datapoint_count,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "storage_class": self.storage_class,
            "file_size_bytes": self.file_size_bytes,
            "exported_at": self.exported_at.isoformat(),
            "etag": self.etag,
        }


def _get_s3_client(region: Optional[str] = None):
    """
    Initialize an AWS S3 client via boto3.

    Returns:
        boto3 client for the s3 service (s3.amazonaws.com).
    """
    target_region = region or DEFAULT_REGION
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=30,
    )
    session = boto3.Session()
    return session.client(
        service_name="s3",
        region_name=target_region,
        config=config,
    )


def _build_s3_key(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    export_format: str,
    dimensions: Optional[Dict[str, str]] = None,
    prefix: str = "metric-snapshots",
) -> str:
    """
    Build an S3 object key for the metric snapshot archive.

    Key format: {prefix}/{namespace}/{metric_name}/{date}/{dimensions_hash}.{ext}

    Args:
        metric_name: CloudWatch metric name.
        namespace: CloudWatch namespace.
        start_time: Snapshot start time.
        end_time: Snapshot end time.
        export_format: Export format identifier.
        dimensions: Optional dimension dict.
        prefix: S3 key prefix (default 'metric-snapshots').

    Returns:
        S3 object key string.
    """
    import hashlib

    date_str = start_time.strftime("%Y/%m/%d")
    ts_hash = hashlib.md5(
        f"{start_time.isoformat()}_{end_time.isoformat()}".encode()
    ).hexdigest()[:8]

    dim_str = ""
    if dimensions:
        dim_str = "_" + "_".join(
            f"{k}={v}" for k, v in sorted(dimensions.items())
        )
        # Truncate long dimension strings
        if len(dim_str) > 100:
            dim_str = "_" + hashlib.md5(dim_str.encode()).hexdigest()[:12]

    ext_map = {
        "json": "json",
        "csv": "csv",
        "json_gzip": "json.gz",
        "csv_gzip": "csv.gz",
    }
    ext = ext_map.get(export_format, "json")

    safe_metric = metric_name.replace("/", "_").replace(" ", "_")
    safe_namespace = namespace.replace("/", "_").replace(" ", "_")

    return f"{prefix}/{safe_namespace}/{safe_metric}/{date_str}/{ts_hash}{dim_str}.{ext}"


def metrics_export_archive(
    bucket: str,
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    datapoints: List[Dict[str, Any]],
    export_format: str = "json",
    storage_class: str = "STANDARD_IA",
    dimensions: Optional[Dict[str, str]] = None,
    region: Optional[str] = None,
    client=None,
    prefix: str = "metric-snapshots",
    server_side_encryption: bool = True,
) -> ExportMetadata:
    """
    Archive exported metric snapshots to AWS S3 managed object storage.

    Serializes metric datapoints to the specified format and uploads to S3
    (s3.amazonaws.com) with configurable storage class and encryption.

    Args:
        bucket: Target S3 bucket name.
        metric_name: CloudWatch metric name.
        namespace: CloudWatch namespace.
        start_time: Snapshot start time.
        end_time: Snapshot end time.
        datapoints: List of metric datapoint dicts to archive.
        export_format: Format ('json', 'csv', 'json_gzip', 'csv_gzip').
        storage_class: S3 storage class (default 'STANDARD_IA').
        dimensions: Optional dimension dict for key construction.
        region: AWS region for S3.
        client: Optional pre-configured S3 boto3 client.
        prefix: S3 key prefix for organization.
        server_side_encryption: Enable SSE-S3 encryption.

    Returns:
        ExportMetadata with S3 location and archive details.

    Raises:
        ValueError: If export_format or storage_class is invalid.
    """
    if export_format not in EXPORT_FORMATS:
        raise ValueError(
            f"Invalid export_format '{export_format}'. "
            f"Valid formats: {EXPORT_FORMATS}"
        )

    if storage_class not in S3_STORAGE_CLASSES:
        raise ValueError(
            f"Invalid storage_class '{storage_class}'. "
            f"Valid classes: {S3_STORAGE_CLASSES}"
        )

    if client is None:
        client = _get_s3_client(region=region)

    # Serialize datapoints to bytes
    content_bytes, content_type = _serialize_datapoints(datapoints, export_format)
    file_size = len(content_bytes)

    # Build S3 key
    s3_key = _build_s3_key(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        export_format=export_format,
        dimensions=dimensions,
        prefix=prefix,
    )

    # Upload to S3
    put_params = {
        "Bucket": bucket,
        "Key": s3_key,
        "Body": content_bytes,
        "ContentType": content_type,
        "StorageClass": storage_class,
    }

    if server_side_encryption:
        put_params["ServerSideEncryption"] = "AES256"

    response = client.put_object(**put_params)

    etag = response.get("ETag", "").strip('"')

    return ExportMetadata(
        bucket=bucket,
        key=s3_key,
        metric_name=metric_name,
        namespace=namespace,
        export_format=export_format,
        datapoint_count=len(datapoints),
        start_time=start_time,
        end_time=end_time,
        storage_class=storage_class,
        file_size_bytes=file_size,
        exported_at=datetime.now(timezone.utc),
        etag=etag if etag else None,
    )


def _serialize_datapoints(
    datapoints: List[Dict[str, Any]],
    export_format: str,
) -> tuple:
    """
    Serialize metric datapoints to bytes in the specified format.

    Args:
        datapoints: List of datapoint dicts with timestamp/value/etc.
        export_format: Target format identifier.

    Returns:
        Tuple of (bytes_content, content_type).
    """
    if export_format == "json":
        content = json.dumps(datapoints, indent=2, default=str).encode("utf-8")
        return content, "application/json"

    elif export_format == "json_gzip":
        raw = json.dumps(datapoints, indent=2, default=str).encode("utf-8")
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
            gz.write(raw)
        return buf.getvalue(), "application/gzip"

    elif export_format == "csv":
        if not datapoints:
            return b"timestamp,value,unit\n", "text/csv"

        fieldnames = list(datapoints[0].keys())
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for dp in datapoints:
            writer.writerow({k: str(v) for k, v in dp.items()})
        return output.getvalue().encode("utf-8"), "text/csv"

    elif export_format == "csv_gzip":
        if not datapoints:
            raw = b"timestamp,value,unit\n"
        else:
            fieldnames = list(datapoints[0].keys())
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for dp in datapoints:
                writer.writerow({k: str(v) for k, v in dp.items()})
            raw = output.getvalue().encode("utf-8")

        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
            gz.write(raw)
        return buf.getvalue(), "application/gzip"

    raise ValueError(f"Unsupported export format: {export_format}")


def archive_metric_series_to_s3(
    bucket: str,
    series,
    export_format: str = "json",
    storage_class: str = "STANDARD_IA",
    region: Optional[str] = None,
    client=None,
    prefix: str = "metric-snapshots",
) -> ExportMetadata:
    """
    Archive a MetricSeries object to S3.

    Convenience wrapper that extracts datapoints from a MetricSeries object
    (from observability_models) and archives them.

    Args:
        bucket: Target S3 bucket name.
        series: MetricSeries object with datapoints.
        export_format: Export format.
        storage_class: S3 storage class.
        region: AWS region.
        client: Optional S3 client.
        prefix: S3 key prefix.

    Returns:
        ExportMetadata for the archived series.
    """
    # Convert MetricSeries datapoints to dicts
    datapoint_dicts = []
    for dp in series.datapoints:
        dp_dict = {
            "timestamp": dp.timestamp.isoformat() if hasattr(dp.timestamp, "isoformat") else str(dp.timestamp),
            "value": dp.value,
            "unit": getattr(dp, "unit", "Count"),
        }
        if hasattr(dp, "sample_count") and dp.sample_count is not None:
            dp_dict["sample_count"] = dp.sample_count
        datapoint_dicts.append(dp_dict)

    # Build dimensions dict from series
    dimensions = {}
    for dim in series.dimensions:
        if isinstance(dim, dict) and "Name" in dim and "Value" in dim:
            dimensions[dim["Name"]] = dim["Value"]

    start_time = series.datapoints[0].timestamp if series.datapoints else datetime.now(timezone.utc)
    end_time = series.datapoints[-1].timestamp if series.datapoints else datetime.now(timezone.utc)

    return metrics_export_archive(
        bucket=bucket,
        metric_name=series.metric_name,
        namespace=series.namespace,
        start_time=start_time,
        end_time=end_time,
        datapoints=datapoint_dicts,
        export_format=export_format,
        storage_class=storage_class,
        dimensions=dimensions,
        region=region,
        client=client,
        prefix=prefix,
    )


def verify_s3_archive(
    bucket: str,
    key: str,
    region: Optional[str] = None,
    client=None,
) -> Optional[Dict[str, Any]]:
    """
    Verify an archived metric snapshot exists in S3 and return its metadata.

    Args:
        bucket: S3 bucket name.
        key: S3 object key.
        region: AWS region.
        client: Optional S3 client.

    Returns:
        Dict with object metadata, or None if not found.
    """
    if client is None:
        client = _get_s3_client(region=region)

    try:
        response = client.head_object(Bucket=bucket, Key=key)
        return {
            "bucket": bucket,
            "key": key,
            "s3_uri": f"s3://{bucket}/{key}",
            "content_length": response.get("ContentLength", 0),
            "storage_class": response.get("StorageClass", "STANDARD"),
            "last_modified": response.get("LastModified"),
            "etag": response.get("ETag", "").strip('"'),
            "server_side_encryption": response.get("ServerSideEncryption"),
        }
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return None
        raise
