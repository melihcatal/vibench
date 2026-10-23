"""
object_metadata.py — Read object metadata / head information from managed object storage.

Concrete provider: Amazon S3 via boto3 SDK.
Provider signals:
  - boto3 S3 head_object call
  - S3 client from storage_client
  - AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY env vars
"""

from botocore.exceptions import ClientError

from storage_client import S3StorageClient
from storage_models import ObjectMetadata


def get_object_metadata(
    bucket: str,
    key: str,
) -> ObjectMetadata:
    """
    Retrieve metadata (HEAD) for an S3 object.

    Parameters
    ----------
    bucket : str
        S3 bucket containing the object.
    key : str
        S3 object key.

    Returns
    -------
    ObjectMetadata
        Normalized metadata including content type, size, last modified, etc.

    Raises
    ------
    FileNotFoundError-like ValueError
        If the object does not exist (404).
    ClientError
        For other S3 errors (permissions, network, etc.).
    """
    client = S3StorageClient(bucket=bucket).get_client()

    try:
        response = client.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404" or error_code == "NoSuchKey":
            return ObjectMetadata(
                bucket=bucket,
                key=key,
                exists=False,
            )
        raise

    return ObjectMetadata.from_s3_head(bucket, key, response)
