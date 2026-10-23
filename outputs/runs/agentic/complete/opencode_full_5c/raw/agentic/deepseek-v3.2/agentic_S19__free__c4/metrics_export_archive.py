import os
import json
import gzip
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, BinaryIO
import tempfile
from google.cloud import storage
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import google.api_core.exceptions


def export_metrics_to_storage(
    metric_name: str,
    project_id: str,
    start_time: datetime,
    end_time: datetime,
    bucket_name: str,
    destination_path: str,
    filters: Optional[Dict[str, str]] = None,
    compression: bool = True,
    format_type: str = "json",
) -> Dict[str, Any]:
    """
    Archive exported metric snapshots in Google Cloud Storage.

    Args:
        metric_name: The metric type name (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        project_id: Google Cloud project ID
        start_time: Start of time window
        end_time: End of time window
        bucket_name: Google Cloud Storage bucket name
        destination_path: Path within bucket to store the export
        filters: Optional resource or metric label filters
        compression: Whether to compress the export
        format_type: Export format ('json', 'csv', 'parquet')

    Returns:
        Dictionary containing export results
    """
    try:
        from .query_metric_window import query_metric_window

        datapoints = query_metric_window(
            metric_name=metric_name,
            project_id=project_id,
            start_time=start_time,
            end_time=end_time,
            filter_labels=filters,
        )

        export_data = {
            "export_metadata": {
                "metric_name": metric_name,
                "project_id": project_id,
                "export_timestamp": datetime.utcnow().isoformat(),
                "time_window": {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                },
                "filters": filters or {},
                "format": format_type,
                "compression": compression,
                "data_point_count": len(datapoints),
            },
            "metric_data": datapoints,
        }

        with tempfile.NamedTemporaryFile(
            mode="wb", delete=False, suffix=".tmp"
        ) as tmp_file:
            tmp_path = tmp_file.name

            if format_type == "json":
                content = json.dumps(export_data, indent=2, default=str).encode("utf-8")
            elif format_type == "csv":
                content = convert_to_csv(export_data)
            else:
                content = json.dumps(export_data, indent=2, default=str).encode("utf-8")

            if compression:
                content = gzip.compress(content)
                destination_path = ensure_extension(destination_path, ".gz")

            tmp_file.write(content)

        storage_client = storage.Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)

        blob = bucket.blob(destination_path)
        blob.upload_from_filename(tmp_path)

        blob_metadata = {
            "metric_name": metric_name,
            "project_id": project_id,
            "export_timestamp": datetime.utcnow().isoformat(),
            "time_window_start": start_time.isoformat(),
            "time_window_end": end_time.isoformat(),
            "data_point_count": str(len(datapoints)),
            "format": format_type,
            "compression": "gzip" if compression else "none",
        }

        blob.metadata = blob_metadata
        blob.patch()

        os.unlink(tmp_path)

        return {
            "success": True,
            "export_details": {
                "metric_name": metric_name,
                "data_points": len(datapoints),
                "storage_location": f"gs://{bucket_name}/{destination_path}",
                "file_size_bytes": blob.size,
                "compression_ratio": calculate_compression_ratio(content, datapoints)
                if compression
                else None,
                "bucket": bucket_name,
                "blob_path": destination_path,
                "export_timestamp": datetime.utcnow().isoformat(),
                "metadata": blob_metadata,
            },
            "download_url": generate_signed_url(blob)
            if can_generate_signed_url()
            else None,
        }

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Google Cloud Storage API error: {e}")
        raise
    except Exception as e:
        print(f"Error exporting metrics to storage: {e}")
        raise


def convert_to_csv(export_data: Dict[str, Any]) -> bytes:
    """
    Convert metric data to CSV format.

    Args:
        export_data: Metric data dictionary

    Returns:
        CSV content as bytes
    """
    import csv
    import io

    datapoints = export_data.get("metric_data", [])

    if not datapoints:
        return b""

    output = io.StringIO()
    writer = csv.writer(output)

    headers = ["timestamp", "value", "metric_type", "resource_type"]

    sample_point = datapoints[0]
    if "resource_labels" in sample_point:
        resource_labels = list(sample_point["resource_labels"].keys())
        headers.extend([f"resource_label_{label}" for label in resource_labels])

    if "metric_labels" in sample_point:
        metric_labels = list(sample_point["metric_labels"].keys())
        headers.extend([f"metric_label_{label}" for label in metric_labels])

    writer.writerow(headers)

    for point in datapoints:
        row = [
            point.get("timestamp"),
            point.get("value"),
            point.get("metric_type"),
            point.get("resource_type"),
        ]

        if "resource_labels" in point:
            for label in resource_labels:
                row.append(point["resource_labels"].get(label, ""))

        if "metric_labels" in point:
            for label in metric_labels:
                row.append(point["metric_labels"].get(label, ""))

        writer.writerow(row)

    return output.getvalue().encode("utf-8")


def ensure_extension(path: str, extension: str) -> str:
    """
    Ensure path has the correct extension.

    Args:
        path: File path
        extension: Desired extension

    Returns:
        Path with correct extension
    """
    if not path.endswith(extension):
        return path + extension
    return path


def calculate_compression_ratio(
    compressed_content: bytes, datapoints: List[Dict[str, Any]]
) -> float:
    """
    Calculate compression ratio.

    Args:
        compressed_content: Compressed content
        datapoints: Original datapoints

    Returns:
        Compression ratio
    """
    if not datapoints:
        return 1.0

    original_size = len(json.dumps(datapoints, default=str).encode("utf-8"))
    compressed_size = len(compressed_content)

    if original_size == 0:
        return 1.0

    return compressed_size / original_size


def generate_signed_url(
    blob: storage.Blob, expiration_hours: int = 24
) -> Optional[str]:
    """
    Generate signed URL for downloading the export.

    Args:
        blob: Cloud Storage blob
        expiration_hours: URL expiration time in hours

    Returns:
        Signed URL or None if not possible
    """
    try:
        url = blob.generate_signed_url(
            expiration=datetime.utcnow() + timedelta(hours=expiration_hours),
            method="GET",
        )
        return url
    except Exception as e:
        print(f"Failed to generate signed URL: {e}")
        return None


def can_generate_signed_url() -> bool:
    """
    Check if signed URLs can be generated.

    Returns:
        True if service account has required permissions
    """
    try:
        storage_client = storage.Client()
        buckets = list(storage_client.list_buckets(max_results=1))
        return True
    except Exception:
        return False


def list_metric_exports(
    bucket_name: str,
    project_id: str,
    prefix: Optional[str] = None,
    metric_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    List metric exports in storage bucket.

    Args:
        bucket_name: Google Cloud Storage bucket name
        project_id: Google Cloud project ID
        prefix: Optional path prefix
        metric_filter: Optional metric name filter

    Returns:
        List of export metadata
    """
    try:
        storage_client = storage.Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)

        blobs = bucket.list_blobs(prefix=prefix)

        exports = []
        for blob in blobs:
            if not blob.name.endswith((".json", ".json.gz", ".csv", ".csv.gz")):
                continue

            metadata = blob.metadata or {}

            if metric_filter and metadata.get("metric_name") != metric_filter:
                continue

            export_info = {
                "blob_name": blob.name,
                "bucket": bucket_name,
                "size_bytes": blob.size,
                "updated": blob.updated,
                "metadata": metadata,
                "storage_class": blob.storage_class,
                "url": f"gs://{bucket_name}/{blob.name}",
            }

            exports.append(export_info)

        return exports

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Error listing metric exports: {e}")
        raise


def download_metric_export(
    bucket_name: str, blob_path: str, project_id: str, local_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Download metric export from storage.

    Args:
        bucket_name: Google Cloud Storage bucket name
        blob_path: Path to blob in bucket
        project_id: Google Cloud project ID
        local_path: Optional local path to save file

    Returns:
        Dictionary containing download results
    """
    try:
        storage_client = storage.Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)

        if not blob.exists():
            raise FileNotFoundError(f"Export not found: gs://{bucket_name}/{blob_path}")

        if local_path is None:
            with tempfile.NamedTemporaryFile(
                mode="wb", delete=False, suffix=".export"
            ) as tmp_file:
                local_path = tmp_file.name

        blob.download_to_filename(local_path)

        metadata = blob.metadata or {}

        is_compressed = (
            blob_path.endswith(".gz") or metadata.get("compression") == "gzip"
        )

        if is_compressed:
            with gzip.open(local_path, "rt", encoding="utf-8") as f:
                content = f.read()
        else:
            with open(local_path, "r", encoding="utf-8") as f:
                content = f.read()

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            data = {"content": content, "format": "raw"}

        return {
            "success": True,
            "local_path": local_path,
            "file_size_bytes": os.path.getsize(local_path),
            "metadata": metadata,
            "data_preview": get_data_preview(data),
            "download_timestamp": datetime.utcnow().isoformat(),
        }

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Error downloading metric export: {e}")
        raise
    except Exception as e:
        print(f"Error downloading metric export: {e}")
        raise


def get_data_preview(data: Any, max_points: int = 5) -> Dict[str, Any]:
    """
    Get preview of downloaded data.

    Args:
        data: Downloaded data
        max_points: Maximum number of data points to include in preview

    Returns:
        Data preview
    """
    if isinstance(data, dict) and "metric_data" in data:
        metric_data = data["metric_data"]
        preview_points = metric_data[:max_points]

        return {
            "total_points": len(metric_data),
            "preview_points": preview_points,
            "export_metadata": data.get("export_metadata", {}),
        }

    return {
        "data_type": type(data).__name__,
        "preview": str(data)[:500] + "..." if len(str(data)) > 500 else str(data),
    }


def delete_old_exports(
    bucket_name: str, project_id: str, days_old: int = 30, prefix: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete old metric exports from storage.

    Args:
        bucket_name: Google Cloud Storage bucket name
        project_id: Google Cloud project ID
        days_old: Delete exports older than this many days
        prefix: Optional path prefix

    Returns:
        Dictionary containing deletion results
    """
    try:
        storage_client = storage.Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)

        cutoff_date = datetime.utcnow() - timedelta(days=days_old)

        blobs = bucket.list_blobs(prefix=prefix)

        deleted = []
        failed = []

        for blob in blobs:
            if blob.updated.replace(tzinfo=None) < cutoff_date:
                try:
                    blob.delete()
                    deleted.append(
                        {
                            "name": blob.name,
                            "updated": blob.updated.isoformat(),
                            "size_bytes": blob.size,
                        }
                    )
                except Exception as e:
                    failed.append(
                        {
                            "name": blob.name,
                            "error": str(e),
                        }
                    )

        return {
            "deleted_count": len(deleted),
            "failed_count": len(failed),
            "deleted": deleted,
            "failed": failed,
            "cutoff_date": cutoff_date.isoformat(),
            "operation_timestamp": datetime.utcnow().isoformat(),
        }

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Error deleting old exports: {e}")
        raise
