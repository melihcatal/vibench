from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from storage_client import get_blob_service_client
import os

def create_presigned_download_url(
    container_name: str, blob_name: str, expiry_minutes: int = 60
) -> str:
    """
    Creates a time-limited signed download URL for a stored object in Azure Blob Storage.

    Args:
        container_name (str): The name of the container.
        blob_name (str): The name of the blob.
        expiry_minutes (int): The number of minutes until the URL expires. Defaults to 60.

    Returns:
        str: The presigned download URL.
    """
    account_name = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")

    if not account_name or not account_key:
        raise ValueError(
            "AZURE_STORAGE_ACCOUNT_NAME and AZURE_STORAGE_ACCOUNT_KEY environment variables must be set."
        )

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes),
    )

    # Construct the full URL with the SAS token
    # The format is typically https://<account_name>.blob.core.windows.net/<container_name>/<blob_name>?<sas_token>
    return f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
