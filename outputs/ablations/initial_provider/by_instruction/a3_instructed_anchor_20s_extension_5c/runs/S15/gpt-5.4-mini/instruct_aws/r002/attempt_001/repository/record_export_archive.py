import boto3


def record_export_archive(bucket_name, key, body):
    client = boto3.client("s3")
    client.put_object(Bucket=bucket_name, Key=key, Body=body if isinstance(body, (bytes, bytearray)) else str(body).encode("utf-8"))
    return {"bucket": bucket_name, "key": key}
