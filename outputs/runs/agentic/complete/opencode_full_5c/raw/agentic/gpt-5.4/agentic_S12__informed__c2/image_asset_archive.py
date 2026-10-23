from __future__ import annotations

import json

from vision_client import s3_client
from vision_models import ArchiveResult


def image_asset_archive(
    bucket: str, object_key: str, artifacts: dict, caption: str
) -> dict:
    client = s3_client()
    body = json.dumps(
        {"artifacts": artifacts, "caption": caption}, ensure_ascii=False
    ).encode("utf-8")
    client.put_object(
        Bucket=bucket,
        Key=object_key,
        Body=body,
        ContentType="application/json; charset=utf-8",
    )
    result = ArchiveResult(
        provider="amazon-s3",
        bucket=bucket,
        object_key=object_key,
        uri=f"s3://{bucket}/{object_key}",
    )
    return result.to_dict()
