from __future__ import annotations

from typing import Optional

from storage_client import (
    get_s3_client,
    list_objects_by_prefix as _list_objects_by_prefix,
)
from storage_models import ListPrefixRequest, ListPrefixResponse


def list_objects_by_prefix(
    bucket: str,
    prefix: str,
    delimiter: Optional[str] = None,
    max_keys: int = 1000,
    start_after: Optional[str] = None,
    client=None,
) -> ListPrefixResponse:
    if client is None:
        client = get_s3_client()

    request = ListPrefixRequest(
        bucket=bucket,
        prefix=prefix,
        delimiter=delimiter,
        max_keys=max_keys,
        start_after=start_after,
    )

    return _list_objects_by_prefix(request, client=client)
