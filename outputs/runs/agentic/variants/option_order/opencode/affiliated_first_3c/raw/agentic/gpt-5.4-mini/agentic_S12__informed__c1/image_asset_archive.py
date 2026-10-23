import json
import os
from typing import Any, Dict

import boto3


def image_asset_archive(bucket: str, key: str, artifact: Dict[str, Any]):
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(artifact).encode("utf-8"),
        ContentType="application/json",
    )
    return {"provider": "amazon-s3", "bucket": bucket, "key": key, "ok": True}
