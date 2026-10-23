from storage_client import get_storage_client
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(
    request: UploadObjectRequest
) -> UploadObjectResponse:
    """Uploads a file or byte stream to Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    if request.file_path:
        blob.upload_from_filename(request.file_path)
    elif request.data:
        blob.upload_from_string(request.data)
    else:
        raise ValueError("Either file_path or data must be provided.")

    blob.reload()
    return UploadObjectResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        size=blob.size,
        self_link=blob.media_link,
    )
