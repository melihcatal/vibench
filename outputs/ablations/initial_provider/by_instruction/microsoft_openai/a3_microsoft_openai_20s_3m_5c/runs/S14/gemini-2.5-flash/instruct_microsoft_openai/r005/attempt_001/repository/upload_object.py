from storage_client import get_blob_service_client
from storage_models import UploadObjectRequest, UploadObjectResponse
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=request.container_name, blob=request.blob_name)

    try:
        # Upload the blob
        upload_result = blob_client.upload_blob(request.data, overwrite=True, content_settings=request.content_settings)
        return UploadObjectResponse(
            success=True,
            e_tag=upload_result.get('etag'),
            last_modified=upload_result.get('last_modified').isoformat() if upload_result.get('last_modified') else None
        )
    except ResourceExistsError:
        # This might happen if overwrite=False, but we set overwrite=True, so less likely
        return UploadObjectResponse(success=False)
    except Exception as e:
        print(f"Error uploading blob: {e}")
        return UploadObjectResponse(success=False)
