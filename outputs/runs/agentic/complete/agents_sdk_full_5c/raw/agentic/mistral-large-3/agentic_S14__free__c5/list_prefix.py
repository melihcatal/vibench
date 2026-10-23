from typing import Tuple, List

from google.cloud import storage

from storage_client import get_storage_client, get_bucket_name
from storage_models import ObjectMetadata, ListPrefixResponse


def list_prefix(prefix: str = "", delimiter: str = "/") -> ListPrefixResponse:
    """
    List objects and prefixes under a Google Cloud Storage bucket prefix.
    
    Args:
        prefix: Prefix to filter objects.
        delimiter: Delimiter to simulate directory-like behavior.
        
    Returns:
        ListPrefixResponse containing objects and prefixes.
    """
    client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
    objects = []
    for blob in blobs:
        objects.append(ObjectMetadata(
            name=blob.name,
            size=blob.size,
            content_type=blob.content_type,
            time_created=blob.time_created,
            updated=blob.updated,
            md5_hash=blob.md5_hash,
            metadata=blob.metadata
        ))

    prefixes = blobs.prefixes

    return ListPrefixResponse(objects=objects, prefixes=prefixes)