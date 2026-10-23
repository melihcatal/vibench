from storage_client import get_storage_client
from storage_models import PresignedUrlRequest


def create_presigned_download_url(request: PresignedUrlRequest) -> str:
    """
    Generates a presigned URL to download an S3 object.
    """
    s3_client = get_storage_client()

    url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": request.storage_object.bucket,
            "Key": request.storage_object.key,
        },
        ExpiresIn=request.expiration,
    )

    return url
