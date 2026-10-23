from storage_client import get_storage_client
from storage_models import PresignedUrl


def create_presigned_download_url(
    bucket_name: str, object_name: str, expiration_seconds: int = 3600
) -> PresignedUrl:
    """
    Generates a presigned URL to download an object from S3.

    :param bucket_name: The name of the S3 bucket.
    :param object_name: The name of the object.
    :param expiration_seconds: Time in seconds for the presigned URL to remain valid.
    :return: A PresignedUrl object.
    """
    s3_client = get_storage_client()
    response = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=expiration_seconds,
    )
    return PresignedUrl(url=response, method="GET")
