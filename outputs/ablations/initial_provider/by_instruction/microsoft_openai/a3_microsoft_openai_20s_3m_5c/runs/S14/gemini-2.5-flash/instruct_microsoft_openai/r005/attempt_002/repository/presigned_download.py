from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from storage_client import AzureStorageClient
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def presigned_download(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    try:
        storage_client = AzureStorageClient()
        # The connection string is available in storage_client, need to parse it to get account name and key
        # For simplicity, assuming the connection string is in format: DefaultEndpointsProtocol=https;AccountName=<name>;AccountKey=<key>;EndpointSuffix=core.windows.net
        conn_string_parts = dict(item.split('=', 1) for item in storage_client.connection_string.split(';') if '=' in item)
        account_name = conn_string_parts.get('AccountName')
        account_key = conn_string_parts.get('AccountKey')

        if not account_name or not account_key:
            return PresignedDownloadResponse(success=False, error="Could not parse account name or key from connection string.")

        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=request.container_name,
            blob_name=request.blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(minutes=request.expiry_minutes)
        )

        blob_client = storage_client.get_blob_client(request.container_name, request.blob_name)
        download_url = f"{blob_client.url}?{sas_token}"
        return PresignedDownloadResponse(success=True, download_url=download_url)
    except Exception as e:
        return PresignedDownloadResponse(success=False, error=str(e))
