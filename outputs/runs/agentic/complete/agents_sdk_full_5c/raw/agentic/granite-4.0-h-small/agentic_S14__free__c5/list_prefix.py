# list_prefix.py
from storage_client import ManagedStorageClient
from storage_models import ListResponse

def list_objects_by_prefix(bucket: str, prefix: str, delimiter: str = '') -> ListResponse:
    """List objects stored under a bucket with the given prefix (and optional delimiter for folder structure).

    Args:
        bucket: Bucket/container name.
        prefix: Prefix to filter object keys.
        delimiter: Optional delimiter to emulate folder hierarchy.

    Returns:
        ListResponse with a list of object key names matching the prefix.
    """
    client = ManagedStorageClient()
    keys = client.list_objects(bucket, prefix=prefix, delimiter=delimiter)
    return ListResponse(Contents=[{'Key': k} for k in keys])
