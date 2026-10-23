from google.cloud import storage
from storage_client import get_gcs_client
from storage_models import ListPrefixRequest, ListPrefixResponse


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    """Lists stored objects under a bucket or container prefix in Google Cloud Storage."""
    client = get_gcs_client()

    blobs = client.list_blobs(
        request.bucket_name, prefix=request.prefix, max_results=request.max_results
    )

    objects_data = []
    for blob in blobs:
        objects_data.append(
            {
                "name": blob.name,
                "size": blob.size,
                "content_type": blob.content_type,
                "updated": blob.updated.isoformat(),
            }
        )

    return ListPrefixResponse(objects=objects_data)
