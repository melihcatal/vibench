import json
from datetime import datetime, timezone

from observability_client import load_config, s3_client


def metrics_export_archive(payload, config=None):
    cfg = load_config(config)
    client = s3_client(config)
    body = json.dumps(payload.get("snapshot", {}), separators=(",", ":")).encode("utf-8")
    key = f"{cfg.key_prefix.rstrip('/')}/{payload['metric']}/{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    client.put_object(Bucket=cfg.bucket, Key=key, Body=body, ContentType="application/json")
    return {"bucket": cfg.bucket, "key": key, "bytes": len(body)}
