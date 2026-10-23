from google.cloud import storage
from dataclasses import dataclass
from typing import List


@dataclass
class ListPrefixResponse:
    objects: List[str]
    prefixes: List[str]


def list_prefix(
    bucket_name: str, prefix: str = "", delimiter: str = "/"
) -> ListPrefixResponse:
    """
    Lists stored objects under a Google Cloud Storage bucket prefix.

    Args:
        bucket_name: Name of the GCS bucket.
        prefix: Prefix to filter objects.
        delimiter: Delimiter to simulate directory-like behavior.

    Returns:
        ListPrefixResponse containing object names and common prefixes.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blobs = client.list_blobs(bucket, prefix=prefix, delimiter=delimiter)
    objects = [blob.name for blob in blobs]
    prefixes = blobs.prefixes

    return ListPrefixResponse(objects=objects, prefixes=prefixes)
