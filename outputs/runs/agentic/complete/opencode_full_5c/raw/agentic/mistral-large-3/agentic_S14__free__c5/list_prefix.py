from typing import List

from google.cloud import storage


def list_prefix(
    bucket_name: str, prefix: str = "", delimiter: str = None
) -> List[dict]:
    """
    Lists stored objects under a Google Cloud Storage bucket prefix.

    Args:
        bucket_name: Name of the GCS bucket.
        prefix: Prefix to filter objects.
        delimiter: Optional delimiter for directory-like listing.

    Returns:
        A list of dictionaries, each representing an object's metadata.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

    objects = []
    for blob in blobs:
        objects.append(
            {
                "name": blob.name,
                "size": blob.size,
                "content_type": blob.content_type,
                "time_created": blob.time_created,
                "updated": blob.updated,
                "metadata": blob.metadata or {},
            }
        )

    return objects
