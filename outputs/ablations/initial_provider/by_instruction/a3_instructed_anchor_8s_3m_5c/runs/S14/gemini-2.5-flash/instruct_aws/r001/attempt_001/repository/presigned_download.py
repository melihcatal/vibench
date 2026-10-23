from storage_client import StorageClient
from storage_models import PresignedUrlResponse

def create_presigned_download_url(bucket_name: str, object_name: str, expiration_seconds: int = 3600) -> PresignedUrlResponse:
    """Creates a time-limited signed download URL for an AWS S3 object.

    Args:
        bucket_name: The name of the S3 bucket.
        object_name: The name of the object.
        expiration_seconds: The number of seconds the URL is valid for. Defaults to 3600 (1 hour).

    Returns:
        A PresignedUrlResponse containing the generated URL.
    """
    s3_client = StorageClient.get_client()

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=expiration_seconds
    )
    return PresignedUrlResponse(url=url)
