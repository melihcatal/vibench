from google.cloud import storage
from storage_client import get_gcs_client
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    """Uploads a file or byte stream to Google Cloud Storage."""
    client = get_gcs_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    blob.upload_from_string(request.data, content_type=request.content_type)

    # Reload blob to get updated metadata like size and media_link
    blob.reload()

    return UploadObjectResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        size=blob.size,
        media_link=blob.media_link,
    )
