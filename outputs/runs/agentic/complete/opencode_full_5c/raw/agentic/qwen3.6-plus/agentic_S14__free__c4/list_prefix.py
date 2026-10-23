from datetime import datetime, timezone
from typing import Optional, List
from storage_client import get_s3_client, validate_bucket_name
from storage_models import ListPrefixRequest, ListPrefixResponse, ObjectSummary


def list_objects_by_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    if not validate_bucket_name(request.bucket):
        return ListPrefixResponse(
            success=False,
            bucket=request.bucket,
            prefix=request.prefix,
            error_message=f"Invalid bucket name: {request.bucket}",
        )

    s3_client = get_s3_client()

    list_kwargs = {
        "Bucket": request.bucket,
        "Prefix": request.prefix,
        "MaxKeys": request.max_keys,
    }

    if request.delimiter:
        list_kwargs["Delimiter"] = request.delimiter

    if request.start_after:
        list_kwargs["StartAfter"] = request.start_after

    try:
        response = s3_client.list_objects_v2(**list_kwargs)

        objects: List[ObjectSummary] = []
        for item in response.get("Contents", []):
            last_modified = item.get("LastModified")
            if last_modified and isinstance(last_modified, datetime):
                if last_modified.tzinfo is None:
                    last_modified = last_modified.replace(tzinfo=timezone.utc)

            obj_summary = ObjectSummary(
                key=item["Key"],
                size=item.get("Size", 0),
                last_modified=last_modified,
                etag=item.get("ETag", "").strip('"'),
                storage_class=item.get("StorageClass"),
            )
            objects.append(obj_summary)

        common_prefixes = []
        for cp in response.get("CommonPrefixes", []):
            common_prefixes.append(cp.get("Prefix", ""))

        return ListPrefixResponse(
            success=True,
            bucket=request.bucket,
            prefix=request.prefix,
            objects=objects,
            common_prefixes=common_prefixes,
            is_truncated=response.get("IsTruncated", False),
            next_continuation_token=response.get("NextContinuationToken"),
            key_count=response.get("KeyCount", len(objects)),
        )
    except Exception as e:
        return ListPrefixResponse(
            success=False,
            bucket=request.bucket,
            prefix=request.prefix,
            error_message=str(e),
        )


def list_prefix(
    bucket: str, prefix: str = "", delimiter: Optional[str] = None, max_keys: int = 1000
) -> ListPrefixResponse:
    request = ListPrefixRequest(
        bucket=bucket,
        prefix=prefix,
        delimiter=delimiter,
        max_keys=max_keys,
    )
    return list_objects_by_prefix(request)
