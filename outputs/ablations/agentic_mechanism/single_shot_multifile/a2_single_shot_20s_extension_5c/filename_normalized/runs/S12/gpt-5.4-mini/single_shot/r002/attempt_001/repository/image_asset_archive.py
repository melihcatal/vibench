import json
import os
from typing import Any, Dict, Optional

import boto3

from vision_client import load_vision_config


def archive_image_artifacts(key_prefix: str, artifact: Dict[str, Any], bucket: Optional[str] = None) -> Dict[str, Any]:
    config = load_vision_config()
    s3_bucket = bucket or os.environ.get("AWS_S3_BUCKET", "")
    if not s3_bucket:
        raise ValueError("AWS_S3_BUCKET is required")
    s3 = boto3.client("s3")
    key = key_prefix.rstrip("/") + "/artifact.json"
    s3.put_object(
        Bucket=s3_bucket,
        Key=key,
        Body=json.dumps(artifact, ensure_ascii=False).encode("utf-8"),
        ContentType="application/json",
    )
    return {"provider": "aws_s3", "bucket": s3_bucket, "key": key, "model": config.vision_model}
