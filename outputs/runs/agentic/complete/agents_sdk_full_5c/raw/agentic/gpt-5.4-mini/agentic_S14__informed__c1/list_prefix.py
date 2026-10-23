from typing import Optional

from storage_client import get_bucket
from storage_models import ListResult, PrefixListRequest


def list_objects_under_prefix(
    prefix: str,
    bucket_name: Optional[str] = None,
    delimiter: Optional[str] = None,
) -> ListResult:
    request = PrefixListRequest(bucket_name=bucket_name, prefix=prefix, delimiter=delimiter)
    bucket = get_bucket(request.bucket_name)
    iterator = bucket.list_blobs(prefix=request.prefix, delimiter=request.delimiter)
    return ListResult(bucket_name=bucket.name, prefix=request.prefix, objects=[blob.name for blob in iterator])
