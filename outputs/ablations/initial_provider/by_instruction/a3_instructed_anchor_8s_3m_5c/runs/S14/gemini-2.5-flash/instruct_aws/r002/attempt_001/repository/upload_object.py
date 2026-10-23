import os
from typing import Union

from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(
    request: UploadObjectRequest,
) -> UploadObjectResponse:
    """Uploads a file or byte stream to AWS S3 managed object storage."""
    s3_client = get_s3_client()
    
    if request.file_path:
        if not os.path.exists(request.file_path):
            raise FileNotFoundError(f"File not found at {request.file_path}")
        extra_args = {}
        if request.content_type:
            extra_args['ContentType'] = request.content_type
        with open(request.file_path, 'rb') as f:
            response = s3_client.upload_fileobj(
                f,
                request.bucket_name,
                request.object_key,
                ExtraArgs=extra_args
            )
    elif request.data:
        extra_args = {}
        if request.content_type:
            extra_args['ContentType'] = request.content_type
        response = s3_client.put_object(
            Bucket=request.bucket_name,
            Key=request.object_key,
            Body=request.data,
            **extra_args
        )
    else:
        raise ValueError("Either file_path or data must be provided.")

    # The upload_fileobj and put_object methods don't return the same structure
    # For simplicity, we'll perform a head_object to get ETag and VersionId if needed
    # or assume success if no exception was raised.
    try:
        head_response = s3_client.head_object(
            Bucket=request.bucket_name,
            Key=request.object_key
        )
        e_tag = head_response.get('ETag', '').strip('\"')
        version_id = head_response.get('VersionId')
    except Exception: # Fallback if head_object fails or is not needed
        e_tag = "unknown"
        version_id = None

    return UploadObjectResponse(
        object_key=request.object_key,
        e_tag=e_tag,
        version_id=version_id,
        upload_success=True,
    )
