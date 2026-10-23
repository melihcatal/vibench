from typing import List, Optional

from botocore.exceptions import BotoCoreError, ClientError

from storage_client import get_s3_client, resolve_bucket_name, resolve_prefix
from storage_models import ListPrefixResponse, ObjectSummary, normalize_list_objects_v2


def list_objects_with_prefix(bucket: str, prefix: str = "", max_items: Optional[int] = None) -> ListPrefixResponse:
    client = get_s3_client()
    bucket_name = resolve_bucket_name(bucket)
    resolved_prefix = resolve_prefix(prefix)
    kwargs = {"Bucket": bucket_name, "Prefix": resolved_prefix}
    if max_items is not None:
        kwargs["MaxKeys"] = int(max_items)
    try:
        result = client.list_objects_v2(**kwargs)
        normalized = normalize_list_objects_v2(result)
        items = [ObjectSummary.from_s3(item) for item in normalized.get("Contents", [])]
        return ListPrefixResponse(bucket=bucket_name, prefix=resolved_prefix, objects=items, is_truncated=bool(normalized.get("IsTruncated", False)), key_count=int(normalized.get("KeyCount", len(items))))
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"failed to list objects for s3://{bucket_name}/{resolved_prefix}: {exc}") from exc


__all__ = ["list_objects_with_prefix"]
