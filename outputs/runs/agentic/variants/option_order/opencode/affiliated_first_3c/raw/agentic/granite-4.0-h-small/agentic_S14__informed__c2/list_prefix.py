import os
import json
from storage_client import StorageClient
from storage_models import StorageModels
from typing import Optional

# Use IBM Cloud Object Storage SDK for listing objects under a prefix
s3 = StorageClient().get_service()

def list_prefix(bucket: str, prefix: str = '', delimiter: str = '', max_keys: int = 1000) -> list[dict]:
    """List stored objects under a bucket or container prefix (IBM COS)."
    # The list_objects_v2 call returns a paginated response; simplify handling by requesting max_keys
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter=delimiter, MaxKeys=max_keys)
    # Normalize and return the list of objects
    return StorageModels.normalize_list_response(response)

# Example usage (uncomment to test)
# print(list_prefix('my-bucket', prefix='documents/'))
