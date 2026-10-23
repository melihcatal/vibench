from datetime import datetime

from storage_client import get_s3_client, validate_bucket_name
from storage_models import ListPrefixRequest, ListPrefixResponse, ObjectSummary


def list_objects_by_prefix(
    bucket: str,
    prefix: str = "",
    delimiter: str = "",
    max_keys: int = 1000,
    start_after: str = None,
    continuation_token: str = None,
) -> ListPrefixResponse:
    client = get_s3_client()
    validate_bucket_name(bucket)

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
        response = client.list_objects_v2(**params)

        objects = []
        for obj in response.get("Contents", []):
            last_modified = obj.get("LastModified")
            if last_modified and isinstance(last_modified, datetime):
                pass
            elif last_modified:
                last_modified = datetime.fromisoformat(
                    last_modified.replace("Z", "+00:00")
                )

            objects.append(
                ObjectSummary(
                    key=obj["Key"],
                    size=obj.get("Size", 0),
                    etag=obj.get("ETag", "").strip('"'),
                    last_modified=last_modified,
                    storage_class=obj.get("StorageClass"),
                    owner=obj.get("Owner", {}).get("DisplayName"),
                )
            )

        common_prefixes = []
        for cp in response.get("CommonPrefixes", []):
            common_prefixes.append(cp.get("Prefix", ""))

        return ListPrefixResponse(
            success=True,
            bucket=bucket,
            prefix=prefix,
            objects=objects,
            common_prefixes=common_prefixes,
            is_truncated=response.get("IsTruncated", False),
            next_continuation_token=response.get("NextContinuationToken"),
            key_count=response.get("KeyCount", len(objects)),
        )

    except Exception as exc:
        return ListPrefixResponse(
            success=False,
            bucket=bucket,
            prefix=prefix,
            error=str(exc),
        )


def list_from_request(request: ListPrefixRequest) -> ListPrefixResponse:
    return list_objects_by_prefix(
        bucket=request.bucket,
        prefix=request.prefix,
        delimiter=request.delimiter,
        max_keys=request.max_keys,
        start_after=request.start_after,
        continuation_token=request.continuation_token,
    )
