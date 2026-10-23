from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from storage_client import StorageClient
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse
import os

def presigned_download(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    client = StorageClient().get_blob_service_client()
    account_name = client.account_name
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

    if not account_key:
        raise ValueError("AZURE_STORAGE_ACCOUNT_KEY environment variable not set for SAS token generation.")

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=request.container_name,
        blob_name=request.blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=request.expiry_minutes)
    )

    # Construct the full URL for the blob with the SAS token
    presigned_url = f"https://{account_name}.blob.core.windows.net/{request.container_name}/{request.blob_name}?{sas_token}"

    return PresignedDownloadResponse(presigned_url=presigned_url)
