from storage_client import get_blob_service_client
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(
        container=request.container_name, blob=request.blob_name
    )

    # Upload the blob, specify content_settings if provided
    if request.content_settings:
        upload_result = blob_client.upload_blob(
            request.data, overwrite=True, content_settings=request.content_settings
        )
    else:
        upload_result = blob_client.upload_blob(request.data, overwrite=True)

    return UploadObjectResponse(
        etag=upload_result.etag, last_modified=str(upload_result.last_modified)
    )
