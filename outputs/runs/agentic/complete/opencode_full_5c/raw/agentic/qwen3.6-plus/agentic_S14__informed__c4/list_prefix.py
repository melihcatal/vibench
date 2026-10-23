from typing import Optional

from storage_client import get_s3_client, get_bucket_name
from storage_models import ListPrefixRequest, ListPrefixResponse, ObjectSummary


def list_prefix(
    prefix: str,
    delimiter: str = "",
    max_keys: int = 1000,
    continuation_token: Optional[str] = None,
    bucket: Optional[str] = None,
) -> ListPrefixResponse:
    if bucket is None:
        bucket = get_bucket_name()

    s3_client = get_s3_client()

    list_kwargs = {
        "Bucket": bucket,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }

    if delimiter:
        list_kwargs["Delimiter"] = delimiter

    if continuation_token:
        list_kwargs["ContinuationToken"] = continuation_token

    try:
        response = s3_client.list_objects_v2(**list_kwargs)

        objects = []
        for item in response.get("Contents", []):
            objects.append(
                ObjectSummary(
                    key=item["Key"],
                    size=item.get("Size", 0),
                    last_modified=item.get("LastModified", ""),
                    etag=item.get("ETag", "").strip('"'),
                    storage_class=item.get("StorageClass", "STANDARD"),
                )
            )

        common_prefixes = [
            cp.get("Prefix", "") for cp in response.get("CommonPrefixes", [])
        ]

        return ListPrefixResponse(
            success=True,
            objects=objects,
            common_prefixes=common_prefixes,
            is_truncated=response.get("IsTruncated", False),
            next_continuation_token=response.get("NextContinuationToken"),
        )
    except Exception as exc:
        return ListPrefixResponse(
            success=False,
            error=str(exc),
        )
