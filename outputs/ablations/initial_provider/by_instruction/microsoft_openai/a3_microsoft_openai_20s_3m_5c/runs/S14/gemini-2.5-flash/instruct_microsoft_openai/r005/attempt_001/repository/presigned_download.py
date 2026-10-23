from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from storage_client import get_blob_service_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def presigned_download(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    blob_service_client = get_blob_service_client()

    try:
        # Get the user delegation key
        # In a real application, you might use a user delegation SAS if you need to revoke access
        # For simplicity, here we'll use an account SAS if connection string is available.
        # If using account key from connection string directly, then use generate_blob_sas
        
        account_name = blob_service_client.account_name
        account_key = blob_service_client.credential.account_key if hasattr(blob_service_client.credential, 'account_key') else None

        if not account_key:
            # Fallback or error if account key is not readily available (e.g., using AAD)
            # For AAD, you would typically generate a user delegation SAS
            print("Account key not found, cannot generate account SAS. Ensure connection string with account key is used.")
            return PresignedDownloadResponse(success=False, url=None)

        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=request.container_name,
            blob_name=request.blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(minutes=request.expiry_minutes)
        )

        blob_client = blob_service_client.get_blob_client(container=request.container_name, blob=request.blob_name)
        download_url = f"{blob_client.url}?{sas_token}"

        return PresignedDownloadResponse(success=True, url=download_url)
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return PresignedDownloadResponse(success=False, url=None)
