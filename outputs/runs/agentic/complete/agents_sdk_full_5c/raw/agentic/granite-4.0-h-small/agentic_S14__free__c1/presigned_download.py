import datetime
from storage_client import ManagedStorageClient

def presigned_download_url(bucket: str, object_key: str, expires_in: int = 3600):
    """Generate a time‑limited presigned download URL for an object.  Uses AWS S3 compatible API via ManagedStorageClient.  """
    client = ManagedStorageClient()
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": object_key},
        ExpiresIn=expires_in,
    )
    return url
