from storage_client import get_gcs_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ObjectSummary


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    client = get_gcs_client()
    bucket = client.bucket(request.bucket_name)

    blobs = client.list_blobs(
        bucket, prefix=request.prefix, max_results=request.max_keys
    )

    object_summaries = []
    for blob in blobs:
        object_summaries.append(
            ObjectSummary(
                object_name=blob.name,
                size=blob.size,
                last_modified=blob.time_created.isoformat(),
            )
        )

    # Google Cloud Storage pagination is handled by iterators, no explicit continuation token for a single call.
    # For simplicity, next_continuation_token is not implemented here.
    return ListPrefixResponse(
        bucket_name=request.bucket_name,
        prefix=request.prefix,
        objects=object_summaries,
        next_continuation_token=None,
    )
