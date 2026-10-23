from storage_client import StorageClient
from storage_models import UploadObjectRequest, UploadObjectResponse
from azure.core.exceptions import ResourceExistsError

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    client = StorageClient().get_blob_service_client()
    blob_client = client.get_blob_client(container=request.container_name, blob=request.blob_name)

    try:
        blob_client.upload_blob(request.data, overwrite=True, content_settings=request.content_settings)
        properties = blob_client.get_blob_properties()
        return UploadObjectResponse(
            message="Object uploaded successfully",
            etag=properties.etag
        )
    except ResourceExistsError:
        properties = blob_client.get_blob_properties()
        return UploadObjectResponse(
            message="Object already exists, overwritten successfully",
            etag=properties.etag
        )
    except Exception as e:
        raise RuntimeError(f"Failed to upload object: {e}")

