from storage_client import get_storage_client
from storage_models import BlobMetadata


def get_object_metadata(bucket_name: str, object_name: str) -> BlobMetadata:
    """
    Retrieves metadata for an object in Google Cloud Storage.

    :param bucket_name: The name of the GCS bucket.
    :param object_name: The name of the object.
    :return: A dictionary containing the object's metadata.
    """
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(object_name)

    if not blob:
        raise ValueError(f"Object '{object_name}' not found in bucket '{bucket_name}'.")

    metadata: BlobMetadata = {
        "name": blob.name,
        "bucket": blob.bucket.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "updated": blob.updated.isoformat(),
    }
    return metadata
