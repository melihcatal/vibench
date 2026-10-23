import os
from storage_client import get_s3_client
from storage_models import ObjectUploadRequest, ObjectUploadResponse

def upload_object(request: ObjectUploadRequest) -> ObjectUploadResponse:
    """Uploads a file or byte stream to AWS S3 managed object storage.

    Args:
        request: An ObjectUploadRequest containing bucket, key, and content.

    Returns:
        An ObjectUploadResponse with ETag and VersionId.
    """
    s3_client = get_s3_client()
    upload_params = {
        'Bucket': request.bucket_name,
        'Key': request.object_key,
    }

    if request.file_path:
        if not os.path.exists(request.file_path):
            raise FileNotFoundError(f"File not found at {request.file_path}")
        with open(request.file_path, 'rb') as f:
            s3_client.upload_fileobj(f, **upload_params)
    elif request.data_bytes:
        s3_client.put_object(Body=request.data_bytes, **upload_params)
    else:
        raise ValueError("Either file_path or data_bytes must be provided for upload.")

    # After upload, we can get the object details to return ETag and VersionId
    # Note: For S3, upload_fileobj/put_object might not return VersionId directly for non-versioned buckets.
    # We'll do a head_object to get full details.
    head_response = s3_client.head_object(
        Bucket=request.bucket_name,
        Key=request.object_key
    )

    etag = head_response['ETag'].strip('\"') # Remove quotes from ETag
    version_id = head_response.get('VersionId')

    return ObjectUploadResponse(etag=etag, version_id=version_id)
