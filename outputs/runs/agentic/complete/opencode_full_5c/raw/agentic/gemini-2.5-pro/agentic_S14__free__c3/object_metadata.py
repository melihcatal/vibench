from storage_client import get_storage_client
from storage_models import S3Object, ObjectMetadata


def get_object_metadata(s3_object: S3Object) -> ObjectMetadata:
    """
    Retrieves metadata for an object in S3.
    """
    s3_client = get_storage_client()
    response = s3_client.head_object(Bucket=s3_object.bucket, Key=s3_object.key)

    return ObjectMetadata(
        content_type=response.get("ContentType", ""),
        content_length=response.get("ContentLength", 0),
        e_tag=response.get("ETag", ""),
        last_modified=str(response.get("LastModified")),
    )
