from storage_client import get_storage_client
from storage_models import StorageObject


def get_object_metadata(bucket_name: str, object_name: str) -> StorageObject:
    """
    Retrieves metadata for an object in S3 without downloading the object itself.

    :param bucket_name: The name of the S3 bucket.
    :param object_name: The name of the object.
    :return: A StorageObject with metadata.
    """
    s3_client = get_storage_client()
    response = s3_client.head_object(Bucket=bucket_name, Key=object_name)

    metadata = {
        "content_length": response.get("ContentLength"),
        "content_type": response.get("ContentType"),
        "etag": response.get("ETag"),
        "last_modified": response.get("LastModified"),
        "custom_metadata": response.get("Metadata", {}),
    }

    return StorageObject(bucket=bucket_name, key=object_name, metadata=metadata)
