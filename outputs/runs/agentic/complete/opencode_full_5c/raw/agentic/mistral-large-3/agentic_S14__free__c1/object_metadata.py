from storage_client import StorageClient
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse


def object_metadata(bucket_name: str, object_key: str) -> ObjectMetadataResponse:
    """
    Reads object metadata from Amazon S3 storage.
    """
    client = StorageClient().get_client()

    request: ObjectMetadataRequest = {
        "bucket_name": bucket_name,
        "object_key": object_key,
    }

    try:
        response = client.head_object(
            Bucket=request["bucket_name"], Key=request["object_key"]
        )
        return {
            "content_type": response.get("ContentType"),
            "content_length": response["ContentLength"],
            "etag": response["ETag"].strip('"'),
            "last_modified": response["LastModified"].isoformat(),
            "metadata": response.get("Metadata", {}),
            "storage_class": response.get("StorageClass", "STANDARD"),
        }
    except Exception as e:
        raise Exception(f"Failed to fetch metadata for S3 object: {str(e)}")
