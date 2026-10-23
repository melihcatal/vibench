"""
Archive exported metric snapshots in managed object storage.

Uses the Google Cloud Storage API (storage.googleapis.com) via the
google-cloud-storage SDK to store and archive metric snapshot data
as timestamped JSON/CSV objects in GCS buckets.
"""

import os
import json
import datetime
from typing import Optional, Dict, Any, List, BinaryIO

from google.cloud import storage


def _get_gcs_client(credentials_path: Optional[str] = None) -> storage.Client:
    """Create and return a Google Cloud Storage client.

    Args:
        credentials_path: Path to GCP service account JSON.
            Defaults to GOOGLE_APPLICATION_CREDENTIALS env var.

    Returns:
        Authenticated google.cloud.storage.Client.

    Raises:
        ValueError: If no credentials are available.
    """
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required "
            "for Google Cloud Storage API access."
        )

    return storage.Client()


def archive_metric_snapshot(
    bucket_name: str,
    metric_name: str,
    snapshot_data: Dict[str, Any],
    blob_prefix: Optional[str] = None,
    credentials_path: Optional[str] = None,
    timestamp: Optional[datetime.datetime] = None,
    content_type: str = "application/json",
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Archive an exported metric snapshot in Google Cloud Storage.

    Uploads metric snapshot data as a JSON object to a GCS bucket
    (storage.googleapis.com) with a timestamped object name for archival.

    Args:
        bucket_name: GCS bucket name for archival storage.
        metric_name: Name of the metric being archived.
        snapshot_data: The metric snapshot data dict to store.
        blob_prefix: Optional prefix path within the bucket.
        credentials_path: Path to GCP service account JSON.
        timestamp: Archive timestamp. Defaults to current UTC time.
        content_type: MIME type for the blob (default: application/json).
        metadata: Optional custom metadata key-value pairs for the blob.

    Returns:
        Dict with 'bucket', 'blob_name', 'size_bytes', 'media_link',
        and 'archived_at' fields.

    Raises:
        ValueError: If no GCP credentials are configured.
    """
    client = _get_gcs_client(credentials_path)
    bucket = client.bucket(bucket_name)

    # Build the blob path with timestamp
    if timestamp is None:
        timestamp = datetime.datetime.now(datetime.timezone.utc)

    ts_str = timestamp.strftime("%Y/%m/%d/%H%M%S")
    if blob_prefix:
        blob_name = f"{blob_prefix.strip('/')}/{metric_name}/{ts_str}/snapshot.json"
    else:
        blob_name = f"metric_snapshots/{metric_name}/{ts_str}/snapshot.json"

    blob = bucket.blob(blob_name)
    blob.content_type = content_type

    # Add standard metadata
    if metadata is None:
        metadata = {}
    metadata["metric_name"] = metric_name
    metadata["archived_at"] = timestamp.isoformat()
    metadata["snapshot_format"] = "json"
    blob.metadata = metadata

    # Upload the snapshot data
    blob.upload_from_string(
        json.dumps(snapshot_data, indent=2, default=str),
        content_type=content_type,
    )

    return {
        "bucket": bucket_name,
        "blob_name": blob_name,
        "size_bytes": blob.size or len(json.dumps(snapshot_data, default=str).encode("utf-8")),
        "media_link": blob.media_link,
        "archived_at": timestamp.isoformat(),
        "metric_name": metric_name,
    }


def archive_metric_snapshot_csv(
    bucket_name: str,
    metric_name: str,
    csv_content: str,
    blob_prefix: Optional[str] = None,
    credentials_path: Optional[str] = None,
    timestamp: Optional[datetime.datetime] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Archive metric snapshot data as a CSV file in GCS.

    Args:
        bucket_name: GCS bucket name.
        metric_name: Name of the metric.
        csv_content: CSV-formatted string data.
        blob_prefix: Optional prefix within the bucket.
        credentials_path: Path to GCP credentials.
        timestamp: Archive timestamp.
        metadata: Optional custom metadata.

    Returns:
        Dict with archival details.
    """
    client = _get_gcs_client(credentials_path)
    bucket = client.bucket(bucket_name)

    if timestamp is None:
        timestamp = datetime.datetime.now(datetime.timezone.utc)

    ts_str = timestamp.strftime("%Y/%m/%d/%H%M%S")
    if blob_prefix:
        blob_name = f"{blob_prefix.strip('/')}/{metric_name}/{ts_str}/snapshot.csv"
    else:
        blob_name = f"metric_snapshots/{metric_name}/{ts_str}/snapshot.csv"

    blob = bucket.blob(blob_name)
    blob.content_type = "text/csv"

    if metadata is None:
        metadata = {}
    metadata["metric_name"] = metric_name
    metadata["archived_at"] = timestamp.isoformat()
    blob.metadata = metadata

    blob.upload_from_string(csv_content, content_type="text/csv")

    return {
        "bucket": bucket_name,
        "blob_name": blob_name,
        "size_bytes": blob.size or len(csv_content.encode("utf-8")),
        "media_link": blob.media_link,
        "archived_at": timestamp.isoformat(),
        "format": "csv",
    }


def list_archived_snapshots(
    bucket_name: str,
    metric_name: Optional[str] = None,
    blob_prefix: Optional[str] = None,
    credentials_path: Optional[str] = None,
    max_results: int = 100,
) -> List[Dict[str, Any]]:
    """List archived metric snapshots in a GCS bucket.

    Args:
        bucket_name: GCS bucket name.
        metric_name: Filter by metric name prefix.
        blob_prefix: Optional blob prefix filter.
        credentials_path: Path to GCP credentials.
        max_results: Maximum number of blobs to return.

    Returns:
        List of dicts with snapshot details.
    """
    client = _get_gcs_client(credentials_path)
    bucket = client.bucket(bucket_name)

    prefix = blob_prefix or ""
    if metric_name:
        if prefix:
            prefix = f"{prefix.strip('/')}/{metric_name}/"
        else:
            prefix = f"metric_snapshots/{metric_name}/"

    blobs = bucket.list_blobs(prefix=prefix, max_results=max_results)

    results = []
    for blob in blobs:
        results.append({
            "bucket": bucket_name,
            "blob_name": blob.name,
            "size_bytes": blob.size or 0,
            "updated": blob.updated.isoformat() if blob.updated else None,
            "content_type": blob.content_type,
            "metadata": blob.metadata or {},
        })

    return results


def download_archived_snapshot(
    bucket_name: str,
    blob_name: str,
    credentials_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Download an archived metric snapshot from GCS.

    Args:
        bucket_name: GCS bucket name.
        blob_name: Full blob path within the bucket.
        credentials_path: Path to GCP credentials.

    Returns:
        Dict with 'content' (parsed JSON or raw bytes) and metadata.
    """
    client = _get_gcs_client(credentials_path)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    content_bytes = blob.download_as_bytes()

    if blob.content_type == "application/json":
        content = json.loads(content_bytes.decode("utf-8"))
    else:
        content = content_bytes

    return {
        "bucket": bucket_name,
        "blob_name": blob_name,
        "content": content,
        "content_type": blob.content_type,
        "size_bytes": blob.size or len(content_bytes),
        "metadata": blob.metadata or {},
        "updated": blob.updated.isoformat() if blob.updated else None,
    }
