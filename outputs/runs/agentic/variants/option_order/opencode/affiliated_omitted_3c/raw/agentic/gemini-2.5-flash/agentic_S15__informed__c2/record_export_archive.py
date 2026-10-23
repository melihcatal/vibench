import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from typing import Any, Dict


def archive_document_snapshot(
    document_id: str,
    snapshot_content: Dict[str, Any],
    container_name: str = "document-snapshots",
) -> str:
    connect_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not connect_str:
        raise ValueError(
            "AZURE_STORAGE_CONNECTION_STRING environment variable not set."
        )

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    try:
        container_client = blob_service_client.get_container_client(container_name)
        container_client.create_container()
    except Exception as e:
        # Container already exists, which is fine.
        pass

    blob_name = f"{document_id}.json"
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    # Convert dict to JSON string and then to bytes
    snapshot_bytes = json.dumps(snapshot_content, indent=2).encode("utf-8")

    blob_client.upload_blob(snapshot_bytes, overwrite=True)

    return blob_client.url
