from storage_client import get_storage_client
from datetime import timedelta

def create_presigned_download_url(bucket: str, key: str, expiration_seconds: int = 3600) -&gt; str:
    """
    Create time-limited presigned download URL for Amazon S3 object.
    """
    client = get_storage_client()
    url = client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration_seconds
    )
    return url