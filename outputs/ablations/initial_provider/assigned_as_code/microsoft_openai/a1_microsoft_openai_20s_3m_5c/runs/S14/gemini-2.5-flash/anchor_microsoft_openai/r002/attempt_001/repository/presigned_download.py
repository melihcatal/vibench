from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from storage_client import get_blob_service_client, get_container_name, get_account_key
from storage_models import PresignedDownloadRequest

def presigned_download(request: PresignedDownloadRequest):
    blob_service_client = get_blob_service_client()
    container_name = get_container_name()

    # Get the blob client for the specific blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=request.object_name)

    # Generate SAS token
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        blob_name=request.object_name,
        account_key=get_account_key(),
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=request.expiry_minutes)
    )

    # Construct the full URL with SAS token
    download_url = f"{blob_client.url}?{sas_token}"

    return {"object_name": request.object_name, "presigned_url": download_url, "expiry_minutes": request.expiry_minutes}
