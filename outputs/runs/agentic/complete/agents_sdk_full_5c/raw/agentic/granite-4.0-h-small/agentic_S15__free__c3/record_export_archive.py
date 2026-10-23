# record_export_archive.py
# [LATER-STEP] Export a document snapshot and store it in Azure Blob Storage

import os
import uuid
import json
from database_client import get_cosmos_db_client
from database_models import DocumentFetchResult
from azure.storage.blob import BlobServiceClient, BlobClient

BLOB_ACCOUNT_URL = os.getenv("BLOB_ACCOUNT_URL")
BLOB_ACCOUNT_KEY = os.getenv("BLOB_ACCOUNT_KEY")
CONTAINER_NAME = "export-snapshots"

if not BLOB_ACCOUNT_URL or not BLOB_ACCOUNT_KEY:
    raise RuntimeError("Blob Storage credentials not configured")

service_client = BlobServiceClient(account_url=BLOB_ACCOUNT_URL, credential=BLOB_ACCOUNT_KEY)
container_client = service_client.get_container_client(CONTAINER_NAME)

if not container_client.exists():
    container_client.create_container()


def export_document_snapshot(document_id: str) -> None:
    """Fetch a document, store a JSON snapshot in Blob Storage, and return the blob URL."""
    client = get_cosmos_db_client()
    container = client.get_container("mydb", "documents")
    # Read the document (includes its ETag for versioning)
    doc = container.read_item(item=document_id, partition_key=document_id)
    # Serialize to JSON
    snapshot = json.dumps(doc, indent=2)
    # Generate a deterministic blob name using UUID + original ID
    blob_name = f"snapshot_{document_id}_{uuid.uuid4().hex[:8]}.json"
    blob_client = BlobClient(account_url=BLOB_ACCOUNT_URL, container_name=CONTAINER_NAME, blob_name=blob_name)
    # Upload the snapshot
    blob_client.upload_blob(snapshot, overwrite=True)
    return f"https://{service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
