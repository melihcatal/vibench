import boto3

client = boto3.client('s3')

def archive_metric_snapshot(bucket_name, file_name, data):
    client.put_object(Bucket=bucket_name, Key=file_name, Body=data)