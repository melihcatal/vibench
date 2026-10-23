from storage_client import AzureBlobStorageClient
from storage_models import UploadObjectRequest, UploadObjectResponse
from azure.core.exceptions import ResourceNotFoundError

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    client = AzureBlobStorageClient()
    try:
        blob_client = client.get_blob_client(request.container_name, request.blob_name)
        response = blob_client.upload_blob(request.data, overwrite=True, content_settings=request.content_settings)
        return UploadObjectResponse(
            success=True,
            blob_url=blob_client.url,
            e_tag=response['etag'],
            last_modified=str(response['last_modified'])
        )
    except ResourceNotFoundError:
        return UploadObjectResponse(success=False, error=f"Container '{request.container_name}' not found.")
    except Exception as e:
        return UploadObjectResponse(success=False, error=str(e))
