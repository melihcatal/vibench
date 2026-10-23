from botocore.exceptions import ClientError
from storage_client import get_storage_client, get_bucket_name
from storage_models import ObjectMetadata

def get_object_metadata(object_name: str, bucket_name: str = None) -> ObjectMetadata:
    """
    Retrieves metadata for an object in S3 using a HEAD request.

    :param object_name: The key of the object in the bucket.
    :param bucket_name: The S3 bucket. Defaults to env config.
    :return: An ObjectMetadata object.
    """
    s3_client = get_storage_client()
    target_bucket = bucket_name or get_bucket_name()

    try:
        response = s3_client.head_object(Bucket=target_bucket, Key=object_name)
        
        metadata = ObjectMetadata(
            key=object_name,
            version_id=response.get("VersionId"),
            size_bytes=response.get("ContentLength"),
            last_modified=response.get("LastModified"),
            content_type=response.get("ContentType"),
            etag=response.get("ETag", "").strip('"'),
            custom_metadata=response.get("Metadata", {}),
        )
        return metadata

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise FileNotFoundError(f"Object '{object_name}' not found in bucket '{target_bucket}'.")
        print(f"Error getting object metadata: {e}")
        raise
