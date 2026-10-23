from storage_client import get_s3_client, validate_bucket_name, handle_s3_error
from storage_models import (
    ListPrefixRequest,
    ListPrefixResponse,
    normalize_list_response,
)


def list_objects_by_prefix(
    bucket: str,
    prefix: str = "",
    delimiter: str = "",
    max_keys: int = 1000,
    start_after: str = "",
    continuation_token: str = None,
    region_name: str = None,
) -> ListPrefixResponse:
    validate_bucket_name(bucket)
    s3 = get_s3_client(region_name=region_name)
    params = {
        "Bucket": bucket,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }
    if delimiter:
        params["Delimiter"] = delimiter
    if start_after:
        params["StartAfter"] = start_after
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    try:
        response = s3.list_objects_v2(**params)
        return normalize_list_response(response, bucket, prefix)
    except Exception as exc:
        handle_s3_error(exc, "list_objects_v2", bucket)


def list_all_objects_by_prefix(
    bucket: str,
    prefix: str = "",
    delimiter: str = "",
    max_keys_per_page: int = 1000,
    region_name: str = None,
) -> ListPrefixResponse:
    validate_bucket_name(bucket)
    s3 = get_s3_client(region_name=region_name)
    all_objects = []
    all_prefixes = []
    is_truncated = False
    next_token = None
    while True:
        params = {
            "Bucket": bucket,
            "Prefix": prefix,
            "MaxKeys": max_keys_per_page,
        }
        if delimiter:
            params["Delimiter"] = delimiter
        if next_token:
            params["ContinuationToken"] = next_token
        try:
            response = s3.list_objects_v2(**params)
        except Exception as exc:
            handle_s3_error(exc, "list_objects_v2", bucket)
        for obj in response.get("Contents", []):
            all_objects.append(obj)
        for cp in response.get("CommonPrefixes", []):
            all_prefixes.append(cp["Prefix"])
        is_truncated = response.get("IsTruncated", False)
        next_token = response.get("NextContinuationToken")
        if not is_truncated:
            break
    merged_response = {
        "Contents": all_objects,
        "CommonPrefixes": [{"Prefix": p} for p in all_prefixes],
        "IsTruncated": False,
        "KeyCount": len(all_objects),
    }
    return normalize_list_response(merged_response, bucket, prefix)


def list_prefix(
    request: ListPrefixRequest, region_name: str = None
) -> ListPrefixResponse:
    return list_objects_by_prefix(
        bucket=request.bucket,
        prefix=request.prefix,
        delimiter=request.delimiter,
        max_keys=request.max_keys,
        start_after=request.start_after,
        region_name=region_name,
    )
