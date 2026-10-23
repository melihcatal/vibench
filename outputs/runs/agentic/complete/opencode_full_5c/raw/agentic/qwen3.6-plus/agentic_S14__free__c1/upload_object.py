from __future__ import annotations

import io
from typing import Optional, Union

from storage_client import get_s3_client, upload_object as _upload_object
from storage_models import UploadRequest, UploadResponse


def upload_object(
    bucket: str,
    key: str,
    data: Union[bytes, io.BytesIO, str],
    content_type: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
    storage_class: str = "STANDARD",
    server_side_encryption: Optional[str] = None,
    client=None,
) -> UploadResponse:
    if client is None:
        client = get_s3_client()

    request = UploadRequest(
        bucket=bucket,
        key=key,
        content_type=content_type,
        metadata=metadata or {},
        storage_class=storage_class,
        server_side_encryption=server_side_encryption,
    )

    return _upload_object(request, data, client=client)
