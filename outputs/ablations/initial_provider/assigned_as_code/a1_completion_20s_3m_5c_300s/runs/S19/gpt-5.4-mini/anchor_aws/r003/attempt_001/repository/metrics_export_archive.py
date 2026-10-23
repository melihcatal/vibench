import boto3


def metrics_export_archive(payload, config=None):
    s3 = boto3.client("s3", region_name=(config or {}).get("region"))
    bucket = payload["bucket"]
    key = payload["key"]
    body = payload.get("body", b"")
    if isinstance(body, str):
        body = body.encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body)
    return {"bucket": bucket, "key": key, "size": len(body)}
