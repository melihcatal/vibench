from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from storage_client import get_blob_service_client
from storage_models import ConfigType, PayloadType
import os

def presigned_download(payload: PayloadType, config: ConfigType = None) -> PayloadType:
    config = config or {}
    account_url = config.get("account_url", os.environ.get("AZURE_STORAGE_ACCOUNT_URL"))
    container_name = config.get("container_name", payload.get("container_name"))
    object_name = payload["object_name"]
    expiry_minutes = payload.get("expiry_minutes", 60) # Default to 60 minutes

    if not all([account_url, container_name, object_name]):
        raise ValueError("Missing required parameters: account_url, container_name, object_name")

    # The SDK's generate_blob_sas function requires the account key.
    # For production scenarios, it's recommended to use a service that provides SAS tokens directly (e.g., Azure Functions)
    # or manage shared access keys securely.
    # For this example, we'll assume the account key is available via environment variable for demonstration.
    account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")
    if not account_key:
        raise ValueError("Azure Storage Account Key not found in environment variables. Required for SAS generation.")

    sas_token = generate_blob_sas(
        account_name=account_url.split('.')[0].split('//')[-1],
        container_name=container_name,
        blob_name=object_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes)
    )

    download_url = f"{account_url}/{container_name}/{object_name}?{sas_token}"

    return {"presigned_url": download_url}
