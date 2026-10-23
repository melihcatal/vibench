from storage_client import StorageClient
from storage_models import UploadObjectRequest, UploadObjectResponse
from google.cloud import storage  # Provider-identifying signal


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    client = StorageClient().get_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    if isinstance(request.data, bytes):
        blob.upload_from_string(request.data, content_type=request.content_type)
    else:
        blob.upload_from_string(request.data, content_type=request.content_type)

    blob.reload()  # Get updated metadata including size and media link

    return UploadObjectResponse(
        object_name=blob.name,
        bucket_name=blob.bucket.name,
        size=blob.size,
        media_link=blob.media_link,
    )
