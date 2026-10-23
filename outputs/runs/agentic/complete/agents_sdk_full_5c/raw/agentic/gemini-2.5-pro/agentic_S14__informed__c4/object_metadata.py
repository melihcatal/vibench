import logging
from botocore.exceptions import ClientError
from storage_client import get_storage_client
from storage_models import ObjectMetadata

# Provider: Amazon S3
# SDK: boto3

def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadata | None:
    """
    Retrieves metadata for an object in an S3 bucket.

    :param bucket_name: The name of the bucket.
    :param object_key: The key of the object.
    :return: ObjectMetadata object, or None if the object does not exist or an error occurs.
    """
    s3_client = get_storage_client()
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        metadata = ObjectMetadata(
            key=object_key,
            size=response["ContentLength"],
            last_modified=response["LastModified"],
            etag=response["ETag"].strip('"'),
            content_type=response.get("ContentType"),
            version_id=response.get("VersionId"),
        )
        return metadata
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            logging.warning(f"Object s3://{bucket_name}/{object_key} not found.")
        else:
            logging.error(f"Error getting metadata for s3://{bucket_name}/{object_key}: {e}")
        return None
