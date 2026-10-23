import os
from storage_client import AzureStorageClient
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    try:
        storage_client = AzureStorageClient()
        blob_client = storage_client.get_blob_client(request.container_name, request.blob_name)

        if request.file_path:
            with open(request.file_path, "rb") as data:
                blob_client.upload_blob(data, metadata=request.metadata, overwrite=True)
        elif request.data is not None:
            blob_client.upload_blob(request.data, metadata=request.metadata, overwrite=True)
        else:
            return UploadObjectResponse(success=False, error="Either file_path or data must be provided.")

        return UploadObjectResponse(success=True, blob_url=blob_client.url)
    except Exception as e:
        return UploadObjectResponse(success=False, error=str(e))
