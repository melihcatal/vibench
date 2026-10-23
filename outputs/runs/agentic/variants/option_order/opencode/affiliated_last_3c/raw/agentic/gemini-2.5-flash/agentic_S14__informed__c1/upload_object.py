from storage_client import get_storage_client
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    if isinstance(request.data, bytes):
        blob.upload_from_string(request.data, content_type=request.content_type)
    else:  # Assume io.BytesIO
        blob.upload_from_file(request.data, content_type=request.content_type)

    blob.reload()  # Get updated metadata including etag and size

    return UploadObjectResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        etag=blob.etag,
        size=blob.size,
    )
