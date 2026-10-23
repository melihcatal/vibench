import os
import uuid
from database_client import get_client
from database_models import DocumentModel
import azure.storage.blob.baseblobservice as azblob

def record_export_archive(document_ids):
    """Archive a list of documents as JSON blobs in Azure Blob Storage.",
    """,
    # Initialize blob service client using environment variables
    account_url = os.getenv("AZURE_STORAGE_ACCOUNT_URL")
    account_key = os.getenv("AZURE_STORAGE_KEY")
    if not account_url or not account_key:
        raise RuntimeError("Azure storage credentials missing")
    service_client = azblob.BlockBlobService(account_name=account_url, account_key=account_key)
    container_name = "archive_container"
    # Create container if it does not exist
    try:
        service_client.create_container(container_name)
    except Exception:
        pass
    container_client = azblob.BlockBlobClient(service_client, container_name)
    for doc_id in document_ids:
        doc = fetch_document(doc_id)
        blob_name = f"snapshots/{doc_id}_{uuid.uuid4().hex}.json"
        container_client.create_blob_from_text(blob_name, json.dumps(doc.data, default=str))
        print(f"Archived {doc_id} to {blob_name}")