import boto3


def metrics_export_archive(
    bucket: str, key: str, body: bytes, content_type: str = "application/json"
) -> dict:
    client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
    return {"bucket": bucket, "key": key, "provider": "Amazon S3"}
