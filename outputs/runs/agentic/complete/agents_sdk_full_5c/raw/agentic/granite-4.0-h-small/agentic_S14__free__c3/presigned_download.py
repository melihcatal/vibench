'''Create a time-limited presigned download URL for an Azure Blob Storage object.'''
import datetime
from azure.storage.blob import BlobServiceClient
from storage_client import get_blob_service_client
from storage_models import PresignedDownloadInfo

def presigned_download(container_name: str, blob_name: str, expiry_minutes: int = 60) -> PresignedDownloadInfo:
    """Generate a presigned URL that allows temporary read access to a blob.

    Args:
        container_name: Name of the container.
        blob_name: Name of the blob to download.
        expiry_minutes: Minutes until the URL expires (default 60).

    Returns:
        A PresignedDownloadInfo object containing the URL and expiration timestamp.
    """
    blob_service_client = get_blob_service_client()
    block_blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry_minutes)
    url = block_blob_client.generate_sas(
        blob=block_blob_client.blob_name,
        account_name=blob_service_client.account_name,
        permission='r',
        expiry=expiry,
    )
    return PresignedDownloadInfo(url=url, expires_at=expiry)
