from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse, normalize_list_objects


def list_objects_with_prefix(bucket: str, prefix: str = "", delimiter: str | None = None, max_keys: int | None = None, s3_client=None) -> ListPrefixResponse:
    client = s3_client or get_s3_client()
    request = ListPrefixRequest(bucket=bucket, prefix=prefix, delimiter=delimiter, max_keys=max_keys)
    kwargs = {"Bucket": request.bucket, "Prefix": request.prefix}
    if request.delimiter is not None:
        kwargs["Delimiter"] = request.delimiter
    if request.max_keys is not None:
        kwargs["MaxKeys"] = request.max_keys
    response = client.list_objects_v2(**kwargs)
    return ListPrefixResponse(**normalize_list_objects(response, request.bucket, request.prefix))
