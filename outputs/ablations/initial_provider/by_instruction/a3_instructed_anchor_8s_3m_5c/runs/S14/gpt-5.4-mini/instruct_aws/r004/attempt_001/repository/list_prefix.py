from storage_client import get_bucket_name, get_s3_client
from storage_models import ListPrefixResponse


def list_objects_with_prefix(bucket=None, prefix="", delimiter=None, max_keys=1000, continuation_token=None):
    client = get_s3_client()
    params = {"Bucket": bucket or get_bucket_name(), "Prefix": prefix, "MaxKeys": max_keys}
    if delimiter is not None:
        params["Delimiter"] = delimiter
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    response = client.list_objects_v2(**params)
    objects = []
    for item in response.get("Contents", []):
        objects.append({"key": item.get("Key"), "size": item.get("Size"), "last_modified": item.get("LastModified"), "etag": item.get("ETag")})
    return ListPrefixResponse(bucket=params["Bucket"], prefix=prefix, objects=objects, is_truncated=response.get("IsTruncated", False), next_token=response.get("NextContinuationToken"))
