import boto3

def archive_metrics_export(bucket_name, file_key, file_content):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=file_content)
    return f's3://{bucket_name}/{file_key}'