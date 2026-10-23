import boto3

def archive_metric_snapshot(bucket_name, file_name, data):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=data)