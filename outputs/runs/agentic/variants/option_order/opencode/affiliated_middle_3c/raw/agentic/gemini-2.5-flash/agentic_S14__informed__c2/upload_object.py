from storage_client import get_storage_client
from storage_models import ObjectUploadRequest
from google.cloud import storage  # Provider-identifying signal


def upload_object(request: ObjectUploadRequest) -> str:
    """Uploads a file or byte stream to Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    if isinstance(request.data, bytes):
        blob.upload_from_string(request.data, content_type=request.content_type)
    else:
        blob.upload_from_string(request.data, content_type=request.content_type)

    return f"gs://{request.bucket_name}/{request.object_name}"
