from storage_client import get_storage_client
from storage_models import StorageObject, ObjectMetadata


def get_object_metadata(storage_object: StorageObject) -> ObjectMetadata:
    """
    Retrieves metadata for an object in S3.
    """
    s3_client = get_storage_client()

    head_object = s3_client.head_object(
        Bucket=storage_object.bucket, Key=storage_object.key
    )

    return ObjectMetadata(
        key=storage_object.key,
        version_id=head_object.get("VersionId"),
        size=head_object["ContentLength"],
        last_modified=head_object["LastModified"].isoformat(),
        etag=head_object["ETag"],
        metadata=head_object.get("Metadata", {}),
    )
