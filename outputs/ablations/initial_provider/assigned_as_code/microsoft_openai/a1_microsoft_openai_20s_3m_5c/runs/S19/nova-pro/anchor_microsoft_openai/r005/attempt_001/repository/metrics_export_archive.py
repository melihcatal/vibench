import boto3


def metrics_export_archive(bucket_name, object_key, data):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)