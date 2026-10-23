from __future__ import annotations

import base64
from pathlib import Path
from typing import Optional, Union

from storage_client import create_s3_client, load_storage_config, normalize_boto_error


def upload_object(key: str, source: Union[str, bytes, bytearray], content_type: Optional[str] = None) -> dict:
    client = create_s3_client()
    bucket = load_storage_config().bucket
    kwargs = {"Bucket": bucket, "Key": key}
    if content_type:
        kwargs["ContentType"] = content_type

    try:
        if isinstance(source, (bytes, bytearray)):
            kwargs["Body"] = bytes(source)
        else:
            path = Path(source)
            kwargs["Body"] = path.read_bytes()
            if content_type is None and path.suffix:
                kwargs["ContentType"] = "application/octet-stream"
        response = client.put_object(**kwargs)
        return {
            "bucket": bucket,
            "key": key,
            "etag": response.get("ETag"),
            "version_id": response.get("VersionId"),
        }
    except Exception as exc:
        return {"error": normalize_boto_error(exc)}


if __name__ == "__main__":
    import os
    import sys

    object_key = os.environ.get("UPLOAD_KEY") or (sys.argv[1] if len(sys.argv) > 1 else None)
    payload = os.environ.get("UPLOAD_DATA")
    if object_key and payload:
        print(upload_object(object_key, base64.b64decode(payload)))
