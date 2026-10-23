from typing import Union
from google.cloud import storage
from storage_client import get_storage_client, get_bucket_name
from storage_models import UploadRequest, UploadResponse


def upload_object(request: UploadRequest) -> UploadResponse:
    """
    Upload a file or byte stream to Google Cloud Storage.
    
    Args:
        request: UploadRequest containing object_name, data, content_type, and metadata.
        
    Returns:
        UploadResponse with object_name and public_url if applicable.
    """
    client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(request.object_name)
    
    blob.upload_from_string(
        request.data,
        content_type=request.content_type,
        metadata=request.metadata
    )
    
    return UploadResponse(
        object_name=request.object_name,
        public_url=blob.public_url,
        size=len(request.data)
    )