import os
from storage_client import StorageClient
from storage_models import UploadRequest


def upload_object(request: UploadRequest) -> str:
    """Uploads a file or byte stream to IBM Cloud Object Storage."""
    client = StorageClient().get_client()
    client.put_object(
        Bucket=request.bucket,
        Key=request.key,
        Body=request.body,
        Metadata=request.metadata,
    )
    return f"cos://{request.bucket}/{request.key}"