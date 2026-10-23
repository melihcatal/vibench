import os
from storage_client import StorageClient
from storage_models import StorageModels

# Use IBM Cloud Object Storage SDK for head object / metadata retrieval
s3 = StorageClient().get_service()

def object_metadata(bucket: str, key: str) -> dict:
    """Read object metadata (head request) from Managed Object Storage (IBM COS)."
    response = s3.head_object(Bucket=bucket, Key=key)
    # Normalize the response into a consistent dict format
    return StorageModels.normalize_metadata_response(response)

# Example usage (uncomment to test)
# print(object_metadata('my-bucket', 'example.txt'))
