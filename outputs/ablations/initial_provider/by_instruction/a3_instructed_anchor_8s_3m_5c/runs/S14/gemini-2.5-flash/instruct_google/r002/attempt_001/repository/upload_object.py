from storage_client import get_storage_client
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.destination_blob_name)

    if request.file_path:
        blob.upload_from_filename(request.file_path, content_type=request.content_type)
    elif request.data:
        blob.upload_from_string(request.data, content_type=request.content_type)
    else:
        raise ValueError("Either 'file_path' or 'data' must be provided for upload.")

    blob.reload()  # Fetch updated metadata after upload

    return UploadObjectResponse(
        bucket_name=request.bucket_name,
        blob_name=request.destination_blob_name,
        public_url=blob.public_url,
        e_tag=blob.etag,
        metadata=blob.metadata
    )
