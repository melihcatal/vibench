from datetime import datetime, timedelta
from azure.storage.blob import BlobClient, generate_blob_sas, BlobSasPermissions
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse
from storage_client import get_blob_service_client

def presigned_download(payload: PresignedDownloadRequest, config: dict = None) -> PresignedDownloadResponse:
    config = config or {}
    account_url = config['account_url']
    container_name = config['container']

    sas_token = generate_blob_sas(
        account_name=account_url.split('.')[0].split('//')[1],
        container_name=container_name,
        blob_name=payload.object_name,
        account_key=config['account_key'], # Azure storage account key is needed for generating SAS token
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=payload.expiry_minutes)
    )

    # Construct the full URL with the SAS token
    blob_client = BlobClient(account_url=account_url, container_name=container_name, blob_name=payload.object_name, credential=None)
    download_url = f"{blob_client.url}?{sas_token}"

    return PresignedDownloadResponse(object_name=payload.object_name, url=download_url)
