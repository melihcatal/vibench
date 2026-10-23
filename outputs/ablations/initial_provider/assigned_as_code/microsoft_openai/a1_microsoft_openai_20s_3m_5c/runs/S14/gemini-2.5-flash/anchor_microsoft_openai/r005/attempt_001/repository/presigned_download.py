from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from storage_client import get_blob_service_client
from storage_models import StoragePresignedUrlResponse
import os

def presigned_download(object_name: str, config: dict, expiry_minutes: int = 60) -> StoragePresignedUrlResponse:
    account_url = config['account_url']
    container_name = config['container']
    account_name = account_url.split('.')[0].split('//')[1] # Extract account name from URL
    
    # The DefaultAzureCredential does not provide a shared key for SAS generation directly.
    # For SAS generation, typically you would use a storage account key.
    # For this example, we'll assume the storage account key is available via an environment variable or config.
    # In a real-world scenario, you might use a managed identity and delegate SAS creation 
    # to a service that has access to the storage account key or can use user delegation SAS.
    
    # For demonstration, we'll use a placeholder for the account key. 
    # In a production environment, NEVER hardcode or expose keys directly.
    # It should be loaded securely, e.g., from Azure Key Vault or environment variables.
    storage_account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")
    if not storage_account_key:
        raise ValueError("AZURE_STORAGE_ACCOUNT_KEY environment variable not set.")

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=object_name,
        account_key=storage_account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes)
    )

    presigned_url = f"{account_url}/{container_name}/{object_name}?{sas_token}"
    return StoragePresignedUrlResponse(object_name=object_name, presigned_url=presigned_url)
