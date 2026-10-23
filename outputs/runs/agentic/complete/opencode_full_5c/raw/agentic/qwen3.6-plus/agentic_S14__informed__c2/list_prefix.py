from typing import Optional

from botocore.exceptions import ClientError

from storage_client import StorageClient
from storage_models import ListObjectsResponse, ObjectSummary


def list_prefix(
    bucket: Optional[str] = None,
    prefix: str = "",
    delimiter: Optional[str] = None,
    max_keys: int = 1000,
    start_after: Optional[str] = None,
    fetch_all: bool = False,
) -> ListObjectsResponse:
    client = StorageClient()
    target_bucket = bucket or client.default_bucket
    if not target_bucket:
        raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

    all_objects: list[ObjectSummary] = []
    all_prefixes: list[str] = []
    continuation_token = None
    is_truncated = False

    try:
        while True:
            list_kwargs = {
                "Bucket": target_bucket,
                "Prefix": prefix,
                "MaxKeys": max_keys,
            }

            if delimiter:
                list_kwargs["Delimiter"] = delimiter

            if start_after:
                list_kwargs["StartAfter"] = start_after

            if continuation_token:
                list_kwargs["ContinuationToken"] = continuation_token

            response = client.s3_client.list_objects_v2(**list_kwargs)

            page_result = ListObjectsResponse.from_s3_list(
                target_bucket, prefix, response, delimiter
            )

            all_objects.extend(page_result.objects)
            all_prefixes.extend(page_result.common_prefixes)
            is_truncated = page_result.is_truncated
            continuation_token = page_result.next_continuation_token

            if not fetch_all or not is_truncated:
                break

        return ListObjectsResponse(
            bucket=target_bucket,
            prefix=prefix,
            objects=all_objects,
            common_prefixes=all_prefixes,
            is_truncated=is_truncated,
            next_continuation_token=continuation_token if is_truncated else None,
            key_count=len(all_objects),
            max_keys=max_keys,
            delimiter=delimiter,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        raise RuntimeError(
            f"Amazon S3 list_objects_v2 failed for s3://{target_bucket}/{prefix}: "
            f"[{error_code}] {error_message}"
        ) from e


def list_all_keys(
    bucket: Optional[str] = None,
    prefix: str = "",
    delimiter: Optional[str] = None,
) -> list[str]:
    result = list_prefix(bucket, prefix, delimiter, fetch_all=True)
    return [obj.key for obj in result.objects]


def count_objects(
    bucket: Optional[str] = None,
    prefix: str = "",
    delimiter: Optional[str] = None,
) -> int:
    result = list_prefix(bucket, prefix, delimiter, fetch_all=True)
    return result.key_count
