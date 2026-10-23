import boto3


def metrics_export_archive(bucket, key, body):
    client = boto3.client("s3")
    return client.put_object(Bucket=bucket, Key=key, Body=body)
