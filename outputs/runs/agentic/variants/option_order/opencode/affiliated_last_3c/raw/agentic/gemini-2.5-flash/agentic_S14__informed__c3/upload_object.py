from storage_client import get_bucket
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    """Uploads a file or byte stream to Google Cloud Storage."""
    bucket = get_bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    blob.upload_from_string(request.data, content_type=request.content_type)

    # Fetch blob metadata to get etag and size
    blob.reload()
    return UploadObjectResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        size=blob.size,
        etag=blob.etag,
    )
