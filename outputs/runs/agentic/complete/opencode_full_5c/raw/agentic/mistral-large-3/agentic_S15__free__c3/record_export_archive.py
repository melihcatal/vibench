from typing import Any, Dict, List
import os
from datetime import datetime
from google.cloud import storage


storage_client = storage.Client()
bucket_name = os.getenv("GCS_BUCKET_NAME", "document-exports")


def archive_document_snapshot(document: Dict[str, Any], snapshot_id: str) -> str:
    """Archives a document snapshot in Google Cloud Storage."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"snapshots/{snapshot_id}_{datetime.now().isoformat()}.json")

    blob.upload_from_string(data=str(document), content_type="application/json")

    return f"gs://{bucket_name}/{blob.name}"


def record_export_archive(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Archives exported document snapshots in Google Cloud Storage."""
    results = []

    for record in records:
        snapshot_id = record["id"]
        archive_url = archive_document_snapshot(record, snapshot_id)
        results.append({"id": record["id"], "archive_url": archive_url})

    return results
