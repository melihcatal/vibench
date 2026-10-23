from storage_client import get_storage_client
from storage_models import PresignedUrlRequest


def create_presigned_download_url(request: PresignedUrlRequest) -> str:
    """
    Generates a presigned URL to download an object from S3.
    """
    s3_client = get_storage_client()

    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": request.s3_object.bucket, "Key": request.s3_object.key},
        ExpiresIn=request.expiration_seconds,
    )
    return url
