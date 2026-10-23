from urllib.parse import urlparse

from database_client import s3_client, load_config


def record_export_archive(payload, config=None):
    cfg = load_config(config)
    client = s3_client(cfg)
    bucket = cfg["bucket_name"]
    key = payload.get("archive_key") or f"exports/{payload['id']}.json"
    body = payload.get("snapshot") or payload.get("document") or {}
    client.put_object(Bucket=bucket, Key=key, Body=str(body).encode("utf-8"))
    parsed = urlparse(f"s3://{bucket}/{key}")
    return {"id": payload.get("id"), "archive_uri": parsed.geturl()}
