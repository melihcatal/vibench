import os
from datetime import datetime, timedelta

from azure.storage.blob import generate_blob_sas, BlobSasPermissions

from storage_client import get_blob_service_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def presigned_download(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    blob_service_client = get_blob_service_client()
    account_name = blob_service_client.account_name
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    if not account_key:
        raise ValueError("AZURE_STORAGE_ACCOUNT_KEY environment variable not set.")

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=request.container_name,
        blob_name=request.blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=request.expiry_minutes)
    )

    blob_url = f"https://{account_name}.blob.core.windows.net/{request.container_name}/{request.blob_name}?{sas_token}"
    return PresignedDownloadResponse(url=blob_url)
