import boto3


def metrics_export_archive(payload, config=None):
    config = config or {}
    client = boto3.client("s3", region_name=config.get("region"))
    bucket = config["bucket"]
    key = payload["key"]
    body = payload["content"].encode("utf-8") if isinstance(payload.get("content"), str) else payload.get("content", b"")
    client.put_object(Bucket=bucket, Key=key, Body=body, ContentType=payload.get("content_type", "application/json"))
    return {"bucket": bucket, "key": key, "size": len(body)}
