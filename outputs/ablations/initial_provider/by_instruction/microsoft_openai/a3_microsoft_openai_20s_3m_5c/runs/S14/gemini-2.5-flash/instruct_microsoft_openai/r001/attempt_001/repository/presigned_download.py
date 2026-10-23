from storage_client import AzureBlobStorageClient
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse
from azure.core.exceptions import ResourceNotFoundError

def presigned_download(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    client = AzureBlobStorageClient()
    try:
        # Verify the blob exists before generating a SAS URL
        blob_client = client.get_blob_client(request.container_name, request.blob_name)
        blob_client.get_blob_properties() # This will raise ResourceNotFoundError if blob/container doesn't exist

        presigned_url = client.generate_sas_url(request.container_name, request.blob_name, request.expiry_minutes)
        return PresignedDownloadResponse(success=True, presigned_url=presigned_url)
    except ResourceNotFoundError:
        return PresignedDownloadResponse(success=False, error=f"Blob '{request.blob_name}' not found in container '{request.container_name}'.")
    except Exception as e:
        return PresignedDownloadResponse(success=False, error=str(e))
