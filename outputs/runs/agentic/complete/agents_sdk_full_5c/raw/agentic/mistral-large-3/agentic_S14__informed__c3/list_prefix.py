from storage_client import get_storage_client
from storage_models import ListPrefixResponse, PrefixObject

def list_objects_with_prefix(bucket_name: str, prefix: str = "", delimiter: str = None) -> ListPrefixResponse:
    """
    Lists stored objects under a Google Cloud Storage bucket prefix.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
    objects = [
        PrefixObject(
            object_key=blob.name,
            size=blob.size,
            last_modified=blob.updated
        )
        for blob in blobs
    ]

    return ListPrefixResponse(
        bucket=bucket_name,
        prefix=prefix,
        objects=objects
    )