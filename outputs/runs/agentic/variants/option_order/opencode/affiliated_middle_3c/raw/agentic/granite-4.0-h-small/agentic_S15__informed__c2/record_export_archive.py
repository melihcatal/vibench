# record_export_archive.py
"""
Later-step implementation file.

Archives exported document snapshots or attachments into managed object storage (Backblaze B2) for durable retention.
"""

import os
import json
import base64
from b2sdk.v1 import InMemoryAccountInfo, B2Api, Bucket, TransferPresets

# Provider configuration from environment variables
B2_APPLICATION_KEY_ID = os.getenv("B2_APPLICATION_KEY_ID")
B2_APPLICATION_KEY = os.getenv("B2_APPLICATION_KEY")
if not B2_APPLICATION_KEY_ID or not B2_APPLICATION_KEY:
    raise RuntimeError("B2_APPLICATION_KEY_ID and B2_APPLICATION_KEY must be set")

# Initialise B2 client
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", B2_APPLICATION_KEY_ID, B2_APPLICATION_KEY)
# Choose a bucket (creates if missing) – you can change bucket name as needed
BUCKET_NAME = os.getenv("B2_BUCKET_NAME", "doc-archive")
bucket: Bucket = b2_api.get_bucket(BUCKET_NAME)


def archive_snapshot(doc_id: str, snapshot_data: dict):
    """
    Upload a JSON snapshot of a document to B2 as a versioned file.

    Args:
        doc_id (str): Identifier of the document.
        snapshot_data (dict): JSON‑serialisable data to store.
    """
    # Encode JSON as base64 to store as a single binary file (optional)
    encoded = base64.b64encode(json.dumps(snapshot_data).encode()).decode()
    file_name = f"snapshot_{doc_id}_{int(os.getenv('ARCHIVE_VERSION', '1'))}.json.b64"
    bucket.upload_file_content(file_name, encoded)


def list_snapshots(doc_id: str) -> list[str]:
    """List all snapshot files belonging to a document ID."""
    results = []
    for file in bucket.list_file_versions():
        if file.file_name.startswith(f"snapshot_{doc_id}_"):
            results.append(file.file_name)
    return results
