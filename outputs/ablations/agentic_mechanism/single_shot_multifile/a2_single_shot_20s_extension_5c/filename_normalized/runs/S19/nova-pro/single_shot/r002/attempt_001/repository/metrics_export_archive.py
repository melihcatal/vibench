import boto3

def archive_metric_snapshot(bucket_name, file_key, file_content):
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=file_content)