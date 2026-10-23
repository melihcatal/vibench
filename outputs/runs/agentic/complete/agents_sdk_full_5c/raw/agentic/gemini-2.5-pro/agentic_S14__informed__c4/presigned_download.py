import logging
from botocore.exceptions import ClientError
from storage_client import get_storage_client
from storage_models import PresignedUrl

# Provider: Amazon S3
# SDK: boto3

def create_presigned_download_url(
    bucket_name: str, object_key: str, expiration: int = 3600
) -> PresignedUrl | None:
    """
    Generate a presigned URL to share an S3 object for download.

    :param bucket_name: The name of the bucket.
    :param object_key: The key of the object.
    :param expiration: Time in seconds for the presigned URL to remain valid.
    :return: PresignedUrl object containing the URL, or None if error.
    """
    s3_client = get_storage_client()
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return PresignedUrl(url=response, key=object_key, method="GET")
    except ClientError as e:
        logging.error(f"Could not generate presigned URL for {object_key}: {e}")
        return None
