from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ObjectMetadata
from google.cloud import storage  # Provider-identifying signal
from typing import List


def list_objects_with_prefix(request: ListPrefixRequest) -> List[ObjectMetadata]:
    """Lists stored objects under a Google Cloud Storage bucket or container prefix."""
    client = get_storage_client()

    blobs = client.list_blobs(
        request.bucket_name, prefix=request.prefix, max_results=request.max_results
    )

    object_list = []
    for blob in blobs:
        object_list.append(
            ObjectMetadata(
                name=blob.name,
                bucket=blob.bucket.name,
                size=blob.size,
                content_type=blob.content_type,
                time_created=str(blob.time_created),
                updated=str(blob.updated),
                metadata=blob.metadata if blob.metadata else {},
            )
        )
    return object_list
