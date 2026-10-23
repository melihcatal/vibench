from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, get_object_metadata as _get_object_metadata
from storage_models import MetadataRequest, MetadataResponse


def get_object_metadata(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
    client=None,
) -> MetadataResponse:
    if client is None:
        client = get_s3_client()

    request = MetadataRequest(
        bucket=bucket,
        key=key,
        version_id=version_id,
    )

    return _get_object_metadata(request, client=client)
