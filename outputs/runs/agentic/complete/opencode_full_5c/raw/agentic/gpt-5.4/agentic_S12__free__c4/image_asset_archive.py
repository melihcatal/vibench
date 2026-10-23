from __future__ import annotations

from typing import Any, Dict

from vision_client import get_archive_bucket, get_s3_client, json_bytes
from vision_models import ArchiveResult, normalize_storage_key


def image_asset_archive(
    image_name: str, artifacts: Dict[str, Any], suffix: str = "analysis"
) -> ArchiveResult:
    s3 = get_s3_client()
    bucket = get_archive_bucket()
    object_key = normalize_storage_key(image_name, suffix)
    s3.put_object(
        Bucket=bucket,
        Key=object_key,
        Body=json_bytes(artifacts),
        ContentType="application/json",
    )
    region = s3.meta.region_name or "us-east-1"
    url = f"https://{bucket}.s3.{region}.amazonaws.com/{object_key}"
    return ArchiveResult(
        provider="amazon-s3", bucket=bucket, object_key=object_key, url=url
    )
