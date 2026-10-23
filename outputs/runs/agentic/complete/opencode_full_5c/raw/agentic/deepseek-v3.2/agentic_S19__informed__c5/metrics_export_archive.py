import os
import json
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional, BinaryIO
from google.cloud import storage
from google.cloud.storage import Blob


def archive_metric_snapshot(
    metric_data: Dict[str, Any],
    bucket_name: str,
    prefix: Optional[str] = None,
    compression: bool = True,
) -> Dict[str, Any]:
    """
    Archive exported metric snapshots in Google Cloud Storage.

    Args:
        metric_data: Metric data to archive
        bucket_name: Google Cloud Storage bucket name
        prefix: Optional path prefix for the archive
        compression: Whether to compress the data

    Returns:
        Dictionary with archive information
    """
    if not metric_data:
        raise ValueError("No metric data provided for archiving")

    try:
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        if not bucket.exists():
            raise ValueError(f"Bucket {bucket_name} does not exist")

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        if prefix:
            prefix = prefix.rstrip("/")
            blob_name = f"{prefix}/metric_snapshot_{timestamp}.json"
        else:
            blob_name = f"metric_snapshot_{timestamp}.json"

        if compression:
            blob_name += ".gz"

        blob = bucket.blob(blob_name)

        data_str = json.dumps(metric_data, indent=2, default=str)

        if compression:
            import gzip

            with tempfile.NamedTemporaryFile(
                mode="wb", suffix=".json.gz", delete=False
            ) as tmp_file:
                with gzip.open(tmp_file.name, "wt", encoding="utf-8") as f:
                    f.write(data_str)
                tmp_file_path = tmp_file.name

            blob.upload_from_filename(tmp_file_path, content_type="application/gzip")
            os.unlink(tmp_file_path)
        else:
            blob.upload_from_string(data_str, content_type="application/json")

        blob.reload()

        archive_info = {
            "bucket": bucket_name,
            "blob_name": blob_name,
            "size_bytes": blob.size,
            "created": blob.time_created.isoformat(),
            "updated": blob.updated.isoformat(),
            "md5_hash": blob.md5_hash,
            "content_type": blob.content_type,
            "compressed": compression,
            "public_url": f"https://storage.googleapis.com/{bucket_name}/{blob_name}",
            "gs_uri": f"gs://{bucket_name}/{blob_name}",
        }

        return archive_info

    except Exception as e:
        raise RuntimeError(f"Failed to archive metric snapshot: {str(e)}")


def batch_archive_metrics(
    metrics_list: List[Dict[str, Any]], bucket_name: str, prefix: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Archive multiple metric snapshots.

    Args:
        metrics_list: List of metric data dictionaries
        bucket_name: Google Cloud Storage bucket name
        prefix: Optional path prefix

    Returns:
        List of archive information dictionaries
    """
    results = []

    for i, metric_data in enumerate(metrics_list):
        try:
            item_prefix = f"{prefix}/batch_{i}" if prefix else f"batch_{i}"
            result = archive_metric_snapshot(metric_data, bucket_name, item_prefix)
            results.append(result)
        except Exception as e:
            results.append({"error": str(e), "index": i, "success": False})

    return results


def list_metric_archives(
    bucket_name: str, prefix: Optional[str] = None, max_results: int = 100
) -> List[Dict[str, Any]]:
    """
    List archived metric snapshots.

    Args:
        bucket_name: Google Cloud Storage bucket name
        prefix: Optional path prefix to filter
        max_results: Maximum number of results to return

    Returns:
        List of archive metadata
    """
    try:
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        if not bucket.exists():
            raise ValueError(f"Bucket {bucket_name} does not exist")

        blobs = storage_client.list_blobs(
            bucket_name, prefix=prefix, max_results=max_results
        )

        archives = []
        for blob in blobs:
            if blob.name.endswith(".json") or blob.name.endswith(".json.gz"):
                archives.append(
                    {
                        "name": blob.name,
                        "size_bytes": blob.size,
                        "created": blob.time_created.isoformat(),
                        "updated": blob.updated.isoformat(),
                        "content_type": blob.content_type,
                        "md5_hash": blob.md5_hash,
                        "compressed": blob.name.endswith(".gz"),
                        "public_url": f"https://storage.googleapis.com/{bucket_name}/{blob.name}",
                        "gs_uri": f"gs://{bucket_name}/{blob.name}",
                    }
                )

        return archives

    except Exception as e:
        raise RuntimeError(f"Failed to list metric archives: {str(e)}")


def retrieve_metric_archive(bucket_name: str, blob_name: str) -> Dict[str, Any]:
    """
    Retrieve an archived metric snapshot.

    Args:
        bucket_name: Google Cloud Storage bucket name
        blob_name: Name of the blob to retrieve

    Returns:
        Dictionary with metric data
    """
    try:
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        if not blob.exists():
            raise ValueError(f"Blob {blob_name} does not exist in bucket {bucket_name}")

        if blob_name.endswith(".gz"):
            import gzip

            compressed_data = blob.download_as_bytes()
            data_str = gzip.decompress(compressed_data).decode("utf-8")
        else:
            data_str = blob.download_as_text()

        metric_data = json.loads(data_str)

        return {
            "data": metric_data,
            "metadata": {
                "bucket": bucket_name,
                "blob_name": blob_name,
                "size_bytes": blob.size,
                "created": blob.time_created.isoformat(),
                "updated": blob.updated.isoformat(),
                "content_type": blob.content_type,
                "compressed": blob_name.endswith(".gz"),
            },
        }

    except Exception as e:
        raise RuntimeError(f"Failed to retrieve metric archive: {str(e)}")


def delete_metric_archive(bucket_name: str, blob_name: str) -> Dict[str, Any]:
    """
    Delete an archived metric snapshot.

    Args:
        bucket_name: Google Cloud Storage bucket name
        blob_name: Name of the blob to delete

    Returns:
        Dictionary with deletion result
    """
    try:
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        if not blob.exists():
            raise ValueError(f"Blob {blob_name} does not exist in bucket {bucket_name}")

        blob.delete()

        return {
            "success": True,
            "bucket": bucket_name,
            "blob_name": blob_name,
            "deleted": True,
            "message": f"Successfully deleted {blob_name} from {bucket_name}",
        }

    except Exception as e:
        raise RuntimeError(f"Failed to delete metric archive: {str(e)}")
