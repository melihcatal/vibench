import json
from datetime import datetime, timezone

import boto3


def metrics_export_archive(payload, config=None):
    config = config or {}
    s3 = boto3.client("s3", region_name=config.get("region"))
    body = json.dumps(payload.get("snapshot", {})).encode("utf-8")
    key = payload.get("key") or f"metrics/{datetime.now(timezone.utc).timestamp()}.json"
    s3.put_object(Bucket=config["bucket"], Key=key, Body=body, ContentType="application/json")
    return {"bucket": config["bucket"], "key": key, "archived": True}
