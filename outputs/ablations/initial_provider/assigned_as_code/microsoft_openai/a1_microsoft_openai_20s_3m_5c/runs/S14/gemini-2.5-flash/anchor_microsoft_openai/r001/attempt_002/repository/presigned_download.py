from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from storage_client import get_blob_service_client
import os

def presigned_download(payload):
    account_name = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")

    if not account_name or not account_key:
        raise ValueError("Azure Storage Account Name or Key not found in environment variables.")

    container_name = payload['container_name']
    object_name = payload['object_name']
    expiry_minutes = payload.get('expiry_minutes', 60)

    # Generate a SAS token for the blob
    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=object_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes)
    )

    # Construct the full SAS URL
    sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{object_name}?{sas_token}"
    
    return {'presigned_url': sas_url, 'object_name': object_name}
