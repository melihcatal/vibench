from typing import Optional

from botocore.exceptions import ClientError

from storage_client import (
    get_s3_client,
    handle_aws_error,
    normalize_list_objects_response,
)
from storage_models import StorageConfig, ListRequest, ListResponse, ListObjectItem


def list_objects_by_prefix(
    bucket: str,
    prefix: str = "",
    delimiter: str = "",
    max_keys: int = 1000,
    start_after: Optional[str] = None,
    config: Optional[StorageConfig] = None,
) -> ListResponse:
    s3_client = get_s3_client(config)

    list_kwargs = {
        "Bucket": bucket,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }

    if delimiter:
        list_kwargs["Delimiter"] = delimiter

    if start_after:
        list_kwargs["StartAfter"] = start_after

    try:
        response = s3_client.list_objects_v2(**list_kwargs)
        normalized = normalize_list_objects_response(response)

        objects = [
            ListObjectItem(
                key=item["key"],
                size=item["size"],
                last_modified=item["last_modified"],
                etag=item["etag"],
                storage_class=item["storage_class"],
            )
            for item in normalized["objects"]
        ]

        return ListResponse(
            success=True,
            objects=objects,
            common_prefixes=normalized["common_prefixes"],
            is_truncated=normalized["is_truncated"],
            next_continuation_token=normalized["next_continuation_token"],
            key_count=normalized["key_count"],
        )

    except ClientError as e:
        return ListResponse(
            success=False,
            error=handle_aws_error(e, "list_objects_by_prefix"),
        )
    except Exception as e:
        return ListResponse(
            success=False,
            error=f"list_objects_by_prefix error: {str(e)}",
        )


def list_all_objects_by_prefix(
    bucket: str,
    prefix: str = "",
    delimiter: str = "",
    config: Optional[StorageConfig] = None,
) -> ListResponse:
    all_objects = []
    all_prefixes = []
    continuation_token = None

    while True:
        result = list_objects_by_prefix(
            bucket=bucket,
            prefix=prefix,
            delimiter=delimiter,
            max_keys=1000,
            start_after=None,
            config=config,
        )

        if not result.success:
            return result

        all_objects.extend(result.objects)
        all_prefixes.extend(result.common_prefixes)

        if not result.is_truncated:
            break

        continuation_token = result.next_continuation_token
        if continuation_token is None:
            break

    return ListResponse(
        success=True,
        objects=all_objects,
        common_prefixes=all_prefixes,
        is_truncated=False,
        key_count=len(all_objects),
    )


def list_objects_from_request(
    request: ListRequest,
    config: Optional[StorageConfig] = None,
) -> ListResponse:
    return list_objects_by_prefix(
        bucket=request.bucket,
        prefix=request.prefix,
        delimiter=request.delimiter,
        max_keys=request.max_keys,
        start_after=request.start_after,
        config=config,
    )
