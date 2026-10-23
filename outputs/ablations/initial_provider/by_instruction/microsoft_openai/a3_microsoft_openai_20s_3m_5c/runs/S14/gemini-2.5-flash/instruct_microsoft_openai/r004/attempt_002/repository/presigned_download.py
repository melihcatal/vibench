import os
from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from storage_client import get_blob_service_client

def generate_presigned_download_url(container_name: str, blob_name: str, expiration_minutes: int = 60):
    blob_service_client = get_blob_service_client()
    account_name = blob_service_client.account_name
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

    if not account_key:
        raise ValueError("AZURE_STORAGE_ACCOUNT_KEY environment variable not set.")

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=expiration_minutes)
    )
    return f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
