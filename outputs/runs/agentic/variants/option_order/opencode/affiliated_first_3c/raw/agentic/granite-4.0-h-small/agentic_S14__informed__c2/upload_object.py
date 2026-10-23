import io
import os
from storage_client import StorageClient
from storage_models import StorageModels

# Use IBM Cloud Object Storage SDK as the concrete provider for same-scenario uploads
s3 = StorageClient().get_service()

def upload_object(bucket: str, key: str, data: bytes, content_type: str = 'application/octet-stream') -> dict:
    """Upload a file or byte stream to Managed Object Storage (IBM COS)."
    # Create an IO stream for the data (supports large payloads via streaming if needed)
    body = io.BytesIO(data)
    # Perform the upload using the SDK's put_object method
    response = s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
    # Return a normalized dict using the helper utilities
    return StorageModels.normalize_upload_response(response)
