import oss2
from storage_client import get_oss_bucket, normalize_prefix
from storage_models import (
    ListPrefixRequest,
    ListPrefixResponse,
    ObjectInfo,
    normalize_oss_object_to_info,
)


def list_objects_by_prefix(
    bucket_name: str,
    prefix: str = "",
    delimiter: str = None,
    max_keys: int = 1000,
    marker: str = None,
) -> ListPrefixResponse:
    prefix = normalize_prefix(prefix) if prefix else ""
    bucket = get_oss_bucket(bucket_name)

    try:
        objects = []
        common_prefixes = []
        is_truncated = False
        next_marker = None

        for obj in oss2.ObjectIterator(
            bucket,
            prefix=prefix,
            delimiter=delimiter,
            max_keys=max_keys,
            marker=marker,
        ):
            if obj.is_prefix():
                common_prefixes.append(obj.key)
            else:
                objects.append(normalize_oss_object_to_info(obj))

        if len(objects) >= max_keys or len(common_prefixes) > 0:
            is_truncated = True
            if objects:
                next_marker = objects[-1].key

        return ListPrefixResponse(
            success=True,
            objects=objects,
            common_prefixes=common_prefixes,
            is_truncated=is_truncated,
            next_marker=next_marker,
        )
    except oss2.exceptions.OssError as e:
        return ListPrefixResponse(
            success=False,
            error=str(e),
        )


def list_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    return list_objects_by_prefix(
        bucket_name=request.bucket,
        prefix=request.prefix,
        delimiter=request.delimiter,
        max_keys=request.max_keys,
        marker=request.marker,
    )
