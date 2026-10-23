import json
from datetime import datetime

import boto3


s3 = boto3.client("s3")


def image_asset_archive(bucket: str, key_prefix: str, image_key: str, analysis: dict, caption: str) -> dict:
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    artifact_key = f"{key_prefix.rstrip('/')}/{timestamp}-analysis.json"
    caption_key = f"{key_prefix.rstrip('/')}/{timestamp}-caption.txt"
    s3.put_object(Bucket=bucket, Key=artifact_key, Body=json.dumps(analysis).encode("utf-8"), ContentType="application/json")
    s3.put_object(Bucket=bucket, Key=caption_key, Body=caption.encode("utf-8"), ContentType="text/plain")
    return {"image_key": image_key, "analysis_key": artifact_key, "caption_key": caption_key}
