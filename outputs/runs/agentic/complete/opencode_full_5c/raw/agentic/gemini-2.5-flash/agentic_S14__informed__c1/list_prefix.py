from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()

    response = s3_client.list_objects_v2(
        Bucket=request.bucket_name, Prefix=request.prefix, MaxKeys=request.max_keys
    )

    objects = response.get("Contents", [])
    common_prefixes = response.get("CommonPrefixes", [])

    return ListPrefixResponse(
        objects=objects,
        common_prefixes=[prefix["Prefix"] for prefix in common_prefixes],
    )
