from storage_client import ManagedStorageClient

def list_objects_with_prefix(bucket: str, prefix: str, delimiter: str = None):
    """List objects under a bucket with a given prefix.  Uses AWS S3 compatible API via ManagedStorageClient.  """
    client = ManagedStorageClient()
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter=delimiter)
    return response.get('Contents', [])
