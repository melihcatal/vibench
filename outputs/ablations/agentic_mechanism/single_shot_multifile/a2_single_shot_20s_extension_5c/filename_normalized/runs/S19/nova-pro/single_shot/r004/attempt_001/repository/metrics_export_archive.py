import boto3

def archive_metric_snapshot(bucket_name, key, data):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=key, Body=data)
    return f's3://{bucket_name}/{key}'