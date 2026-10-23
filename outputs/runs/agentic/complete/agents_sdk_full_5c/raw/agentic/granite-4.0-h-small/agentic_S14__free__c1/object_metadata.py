from storage_client import ManagedStorageClient

def get_object_metadata(bucket: str, object_key: str):
    """Retrieve metadata/HEAD information for an object.  Uses AWS S3 compatible API via ManagedStorageClient.  """
    client = ManagedStorageClient()
    metadata = client.head_object(Bucket=bucket, Key=object_key)
    return metadata
