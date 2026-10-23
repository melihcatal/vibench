import boto3


def metrics_export_archive(bucket, key, body, content_type="application/json"):
    client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
    return {"bucket": bucket, "key": key}
