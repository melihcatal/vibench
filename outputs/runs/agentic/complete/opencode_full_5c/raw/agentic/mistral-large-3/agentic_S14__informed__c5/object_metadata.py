from google.cloud import storage
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class ObjectMetadataResponse:
    name: str
    size_bytes: int
    content_type: str
    time_created: str
    updated: str
    metadata: Dict[str, str]
    etag: str
    generation: str
    metageneration: str


def object_metadata(bucket_name: str, object_name: str) -> ObjectMetadataResponse:
    """
    Reads object metadata from Google Cloud Storage.

    Args:
        bucket_name: Name of the GCS bucket.
        object_name: Name of the object in the bucket.

    Returns:
        ObjectMetadataResponse containing metadata and head information.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.reload()  # Ensure metadata is fresh

    return ObjectMetadataResponse(
        name=blob.name,
        size_bytes=blob.size,
        content_type=blob.content_type,
        time_created=str(blob.time_created),
        updated=str(blob.updated),
        metadata=blob.metadata or {},
        etag=blob.etag,
        generation=str(blob.generation),
        metageneration=str(blob.metageneration),
    )
