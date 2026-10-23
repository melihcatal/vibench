from storage_client import get_storage_client
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(
    request: UploadObjectRequest
) -> UploadObjectResponse:
    """Uploads a file or byte stream to Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    blob.upload_from_string(request.data, content_type=request.content_type)

    # Reload the blob to get updated metadata after upload
    blob.reload()

    return UploadObjectResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        size=blob.size,
        md5_hash=blob.md5_hash, # Google Cloud Storage provides this
        crc32c_hash=blob.crc32c, # Google Cloud Storage provides this
        media_link=blob.media_link
    )
