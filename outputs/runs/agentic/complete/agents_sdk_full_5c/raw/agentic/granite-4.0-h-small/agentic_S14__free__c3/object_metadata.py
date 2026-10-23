'''Retrieve metadata / HEAD information for an Azure Blob Storage object.'''
from azure.storage.blob import BlobServiceClient
from storage_client import get_blob_service_client
from storage_models import ObjectMetadataResult

def object_metadata(container_name: str, blob_name: str) -> ObjectMetadataResult:
    """Return metadata for a blob using HEAD request.

    Args:
        container_name: Name of the container.
        blob_name: Name of the blob.

    Returns:
        ObjectMetadataResult containing properties such as size, last_modified, content_type, etc.
    """
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    props = blob_client.get_blob_properties()
    return ObjectMetadataResult(
        container=container_name,
        blob=blob_name,
        size=props.size,
        last_modified=props.last_modified,
        content_type=props.content_type,
        etag=props.etag,
        metadata=dict(props.metadata) if props.metadata else None,
    )
